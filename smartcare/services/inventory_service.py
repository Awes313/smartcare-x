"""Medicine inventory logic: stock deduction on prescribing, restocking, low-stock alerts."""

from datetime import datetime

from smartcare.extensions import db
from smartcare.models.medicine import Medicine, MedicineInventory


class InsufficientStockError(Exception):
    pass


def deduct_stock(medicine_id, quantity):
    inventory = MedicineInventory.query.filter_by(medicine_id=medicine_id).first()
    if inventory is None:
        raise InsufficientStockError("No inventory record found for this medicine.")

    # Atomic conditional UPDATE — the availability check (quantity_in_stock
    # >= quantity) and the decrement happen in ONE database statement, so
    # two concurrent prescriptions for the same low-stock medicine can't
    # both read "5 available" and both subtract 5, driving stock negative.
    # Whichever request's UPDATE runs first wins; the second sees rowcount
    # == 0 (the WHERE clause no longer matches) and fails cleanly instead
    # of corrupting the stock count.
    result = db.session.execute(
        db.update(MedicineInventory)
        .where(
            MedicineInventory.medicine_id == medicine_id,
            MedicineInventory.quantity_in_stock >= quantity,
        )
        .values(quantity_in_stock=MedicineInventory.quantity_in_stock - quantity)
    )

    if result.rowcount == 0:
        db.session.rollback()
        raise InsufficientStockError(
            f"Insufficient stock for {inventory.medicine.name}: "
            f"{inventory.quantity_in_stock} available, {quantity} requested."
        )

    db.session.commit()
    db.session.refresh(inventory)
    return inventory


def restock(medicine_id, quantity):
    inventory = MedicineInventory.query.filter_by(medicine_id=medicine_id).first()
    if inventory is None:
        inventory = MedicineInventory(medicine_id=medicine_id, quantity_in_stock=0)
        db.session.add(inventory)

    inventory.quantity_in_stock += quantity
    inventory.last_restocked_at = datetime.utcnow()
    db.session.commit()
    return inventory


def get_low_stock_items():
    return (
        MedicineInventory.query.join(Medicine)
        .filter(MedicineInventory.quantity_in_stock <= MedicineInventory.reorder_level)
        .order_by(MedicineInventory.quantity_in_stock.asc())
        .all()
    )
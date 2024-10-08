-- Write a SQL script that creates a trigger that decreases the quantity
-- of an item after adding a new order
DROP TRIGGER IF EXISTS decrease_quantity;
DELIMITER $$
CREATE DELIMITER decrease_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name;
END $$;
DELIMITER;
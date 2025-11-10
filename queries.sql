INSERT INTO users (username, password_hash, first_name, last_name, email, role_id, is_active) VALUES
-- Super Admin
('admin', '$2b$10$rKvVLz6JQxZqJY5y5Z5Z5uYKZJxm7fK3vZJ5Z5Z5Z5Z5Z5Z5Z5Z5', 'Kwame', 'Mensah', 'kmensah@posghana.com', 1, 1),

-- Managers
('manager1', '$2b$10$YYGg7fK3vZJ5Z5Z5Z5Z5ZuX8QNm9pL2wKj6Z5Z5Z5Z5Z5Z5Z5Z5', 'Ama', 'Osei', 'aosei@posghana.com', 2, 1),
('manager2', '$2b$10$pL2wKj6Z5Z5Z5Z5Z5Z5Z5uL9Rm3qN4xPk7Z5Z5Z5Z5Z5Z5Z5Z5', 'Kofi', 'Asante', 'kasante@posghana.com', 2, 1),

-- Cashiers
('cashier1', '$2b$10$qN4xPk7Z5Z5Z5Z5Z5Z5Z5uM2Sn5rO6yQl8Z5Z5Z5Z5Z5Z5Z5Z5', 'Akua', 'Boateng', 'aboateng@posghana.com', 3, 1),
('cashier2', '$2b$10$rO6yQl8Z5Z5Z5Z5Z5Z5Z5uN3To7sP8zRm9Z5Z5Z5Z5Z5Z5Z5Z5', 'Yaw', 'Owusu', 'yowusu@posghana.com', 3, 1),
('cashier3', '$2b$10$sP8zRm9Z5Z5Z5Z5Z5Z5Z5uO4Up9tQ2aSn3Z5Z5Z5Z5Z5Z5Z5Z5', 'Abena', 'Agyemang', 'aagyemang@posghana.com', 3, 1),

-- Stock Keepers
('stock_keeper1', '$2b$10$tQ2aSn3Z5Z5Z5Z5Z5Z5Z5uP5Vq3uR4bTo5Z5Z5Z5Z5Z5Z5Z5Z5', 'Kwabena', 'Nkrumah', 'knkrumah@posghana.com', 4, 1),
('stock_keeper2', '$2b$10$uR4bTo5Z5Z5Z5Z5Z5Z5Z5uQ6Ws5vS6cUp7Z5Z5Z5Z5Z5Z5Z5Z5', 'Adjoa', 'Addo', 'aaddo@posghana.com', 4, 1);
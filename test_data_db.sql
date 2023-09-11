INSERT INTO hotels (name, location, services, number_of_rooms, image_id) VALUES
('La Rocaille', 'Anse Soleil Road, Anse Gouvernement, Baie Lazare, 0000 Baie Lazare Mahé, Seychelles', '["Free WiFi", "Mountain view", "Free parking", "Room Amenities"]', 2, 1),
('Holiday Home', 'Dame Le Roi, Baie Lazare Mahé, Seychelles', '["Free WiFi", "BBQ facilities", "Free parking"]', 4, 2),
('Kanasuk Self catering Apartments', 'Kanasuk Self catering Apartments', '["Free WiFi", "BBQ facilities", "Free parking"]', 8, 3),
('Four Seasons Resort Seychelles', 'Petite Anse, Mahe, Baie Lazare Mahé, Seychelles', '["Free WiFi", "Sea view", "Pool", "Restaurants & cafes"]', 50, 4);


INSERT INTO rooms (hotel_id, name, description, price, quantity, services, image_id) VALUES
(1, 'One-Bedroom House', 'Featuring a terrace with outdoor seating, this house also includes a well-equipped kitchen with oven, microwave and coffee machine. There is a dining area and a sofa with TV. A washing machine is also available.', 100, 1, '["Free WiFi", "Mountain view", "Free parking", "Room Amenities"]', 5),
(1, 'One-Bedroom Chalet', 'This chalet has a terrace and comes with a kitchen, dining area and is located on the ground floor.', 90, 1, '["Free WiFi", "Mountain view", "Free parking", "Room Amenities"]', 6),
(2, 'Villa with Garden View', 'Boasting a private entrance, this air-conditioned villa features a kitchen, 1 bedroom and 1 bathroom with a walk-in shower and a hairdryer.', 100, 2, '["Free WiFi", "Mountain view", "Free parking", "Room Amenities"]', 7),
(2, 'Villa', 'Boasting a private entrance, this air-conditioned villa comes with 1 living room, 2 separate bedrooms and 1 bathroom with a walk-in shower and a hairdryer. ', 90, 2, '["Free WiFi", "Mountain view", "Free parking", "Room Amenities"]', 8),
(3, 'Apartment with Terrace', 'Featuring a terrace with outdoor seating, this house also includes a well-equipped kitchen with oven, microwave and coffee machine. There is a dining area and a sofa with TV. A washing machine is also available.', 100, 4, '["Free WiFi", "Mountain view", "Free parking", "Room Amenities"]', 9),
(3, 'Apartment', 'This chalet has a terrace and comes with a kitchen, dining area and is located on the ground floor.', 90, 4, '["Free WiFi", "Mountain view", "Free parking", "Room Amenities"]', 10),
(4, 'Villa with Ocean View - Hilltop', 'This air-conditioned villa features a wrap around deck and a private pool with a view of the Indian Ocean and the surrounding tropical forest. It comes equipped with a satellite TV, minibar and tea-and-coffee-making facilities.', 1000, 25, '["Free WiFi", "Sea view", "Pool", "Restaurants & cafes"]', 11),
(4, 'Serenity Villa with King Bed', 'Known as the Serenity Villa, this secluded villa offers prime views of the Indian Ocean and tropical forest below.', 900, 25, '["Free WiFi", "Sea view", "Pool", "Restaurants & cafes"]', 12);

INSERT INTO users (email, hashed_password) VALUES
('stefan@travel.com', 'hashed_password_1'),
('fedor@travel.com', 'hashed_password_2'),
('polina@travel.com', 'hashed_password_3');


INSERT INTO bookings (room_id, user_id, date_from, date_to, price) VALUES
(5, 3, '2023-09-15', '2023-09-30', 80),
(5, 2, '2023-09-25', '2023-10-10', 80),
(5, 1, '2023-10-15', '2023-10-30', 80);
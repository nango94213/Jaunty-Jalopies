-- INSERT INTO Manufacturer VALUES ('{name}');
INSERT INTO Manufacturer VALUES ('Acura');
INSERT INTO Manufacturer VALUES ('Alfa Romeo');
INSERT INTO Manufacturer VALUES ('Aston Martin');
INSERT INTO Manufacturer VALUES ('Audi');
INSERT INTO Manufacturer VALUES ('Bentley');
INSERT INTO Manufacturer VALUES ('BMW');
INSERT INTO Manufacturer VALUES ('Buick');
INSERT INTO Manufacturer VALUES ('Cadillac');
INSERT INTO Manufacturer VALUES ('Chevrolet');
INSERT INTO Manufacturer VALUES ('Chrysler');
INSERT INTO Manufacturer VALUES ('Dodge');
INSERT INTO Manufacturer VALUES ('Ferrari');
INSERT INTO Manufacturer VALUES ('FIAT');
INSERT INTO Manufacturer VALUES ('Ford');
INSERT INTO Manufacturer VALUES ('Freightliner');
INSERT INTO Manufacturer VALUES ('Genesis');
INSERT INTO Manufacturer VALUES ('GMC');
INSERT INTO Manufacturer VALUES ('Honda');
INSERT INTO Manufacturer VALUES ('Hyundai');
INSERT INTO Manufacturer VALUES ('INFINITI');
INSERT INTO Manufacturer VALUES ('Jaguar');
INSERT INTO Manufacturer VALUES ('Jeep');
INSERT INTO Manufacturer VALUES ('Kia');
INSERT INTO Manufacturer VALUES ('Lamborghini');
INSERT INTO Manufacturer VALUES ('Land Rover');
INSERT INTO Manufacturer VALUES ('Lexus');
INSERT INTO Manufacturer VALUES ('Lincoln');
INSERT INTO Manufacturer VALUES ('Lotus');
INSERT INTO Manufacturer VALUES ('Maserati');
INSERT INTO Manufacturer VALUES ('Mazda');
INSERT INTO Manufacturer VALUES ('McLaren');
INSERT INTO Manufacturer VALUES ('Mercedes-Benz');
INSERT INTO Manufacturer VALUES ('MINI');
INSERT INTO Manufacturer VALUES ('Mitsubishi');
INSERT INTO Manufacturer VALUES ('Nissan');
INSERT INTO Manufacturer VALUES ('Porsche');
INSERT INTO Manufacturer VALUES ('Ram');
INSERT INTO Manufacturer VALUES ('Rolls-Royce');
INSERT INTO Manufacturer VALUES ('SAAB');
INSERT INTO Manufacturer VALUES ('smart');
INSERT INTO Manufacturer VALUES ('Subaru');
INSERT INTO Manufacturer VALUES ('Tesla');
INSERT INTO Manufacturer VALUES ('Toyota');
INSERT INTO Manufacturer VALUES ('Vauxhall');
INSERT INTO Manufacturer VALUES ('Volkswagen');
INSERT INTO Manufacturer VALUES ('Volvo');


-- INSERT INTO Vehicle 
-- VALUES ('{vin}', '{description}', '{invoice_price}', '{type}', '{model_year}', '{model_name}', '{date_added}', '{clerk_username}', '{manufacturer_name}');
-- SUVs
INSERT INTO Vehicle VALUES ('5TFET54117X016058', '2021 Toyota RAV4', '26350', 'SUV', '2021', 'RAV4', '2021-06-11', 'luis', 'Toyota');
INSERT INTO Vehicle VALUES ('2T1BR30E273767487', '2020 Toyota 4Runner', '36120', 'SUV', '2020', '4Runner', '2021-05-09', 'luis', 'Toyota');
INSERT INTO Vehicle VALUES ('JM1GC2210E1604771', '2021 Mazda CX-30', '22050', 'SUV', '2021', 'CX-30', '2021-03-28', 'luis', 'Mazda');
INSERT INTO Vehicle VALUES ('YV2A4B1C5VA264304', '2022 Volvo XC-40', '34100', 'SUV', '2022', 'XC-40', '2021-11-05', 'luis', 'Volvo');
INSERT INTO Vehicle VALUES ('WBAAF9310MEE65124', '2022 BMW X1', '35400', 'SUV', '2022', 'X1', '2021-10-05', 'luis', 'BMW');

-- Vans
INSERT INTO Vehicle VALUES ('3G1JD5SH0E0013280', '2021 Chevrolet Express', '33000', 'Van', '2021', 'Express', '2021-04-10', 'luis', 'Chevrolet');
INSERT INTO Vehicle VALUES ('4TAWN74N2YZ581143', '2021 RAM ProMaster City', '25715', 'Van', '2021', 'ProMasret City', '2021-06-22', 'luis', 'Ram');
INSERT INTO Vehicle VALUES ('1N6SD16Y2MC404130', '2021 Nisssan NV Cargo', '30640', 'Van', '2021', 'NV Cargo', '2021-09-12', 'luis', 'Nissan');

-- Trucks
INSERT INTO Vehicle VALUES ('5YJSA1CG3DFP14555', '2022 Tesla Cybertruck', '39900', 'Truck', '2022', 'Cybertruck', '2021-11-14', 'luis', 'Tesla');
INSERT INTO Vehicle VALUES ('2FMZA514628322040', '2021 Ford F-150', '29290', 'Truck', '2021', 'F-150', '2021-05-15', 'luis', 'Ford');
INSERT INTO Vehicle VALUES ('9C2KE02007R001317', '2021 Honda Ridgeline', '36490', 'Truck', '2021', 'Ridgeline', '2021-09-10', 'luis', 'Honda');

-- Convertibles
INSERT INTO Vehicle VALUES ('JM2UF2138N0251579', '2021 Mazda MX-5 Miata', '26830', 'Convertible', '2021', 'MX-5 Miata', '2021-06-06', 'luis', 'Mazda');
INSERT INTO Vehicle VALUES ('WP0CB2961NS702088', '2021 Porsche 911', '99200', 'Convertible', '2021', '911', '2021-02-15', 'luis', 'Porsche');
INSERT INTO Vehicle VALUES ('JTHBP5C23D5010933', '2021 Lexus LC', '93050', 'Convertible', '2021', 'LC', '2021-05-09', 'luis', 'Lexus');

-- Car
INSERT INTO Vehicle VALUES ('KM8SG13D27U108692', '2021 Hyundai Elantra', '19650', 'Car', '2021', 'Elantra', '2021-06-07', 'luis', 'Hyundai');
INSERT INTO Vehicle VALUES ('JHMBE376055202903', '2021 Honda Accord', '24970', 'Car', '2021', 'Accord', '2021-04-07', 'luis', 'Honda');
INSERT INTO Vehicle VALUES ('5J8TB4H30DL000860', '2021 Acura TLX', '37500', 'Car', '2021', 'TLX', '2021-04-09', 'luis', 'Acura');

-- Drivetrain type can be: FWD, RWD, AWD
-- INSERT INTO SUV VALUES ('{vin}', '{number_of_cup_holders}', '{drivetrain_type}');
INSERT INTO SUV VALUES ('5TFET54117X016058', '3', 'FWD');
INSERT INTO SUV VALUES ('2T1BR30E273767487', '2', 'AWD');
INSERT INTO SUV VALUES ('JM1GC2210E1604771', '2', 'RWD');
INSERT INTO SUV VALUES ('YV2A4B1C5VA264304', '4', 'FWD');
INSERT INTO SUV VALUES ('WBAAF9310MEE65124', '4', 'AWD');

-- INSERT INTO Van VALUES ('{vin}', '{has_driver_side_backdoor}');
INSERT INTO Van VALUES ('3G1JD5SH0E0013280', TRUE);
INSERT INTO Van VALUES ('4TAWN74N2YZ581143', FALSE);
INSERT INTO Van VALUES ('1N6SD16Y2MC404130', TRUE);

-- Cargo cover types can be: roll-up, soft folding, hard folding, retractable, high impact plastic lid, painted fiberglass lid
-- For number of axles: Most cars have four tires in total, or two sets of tires, with one in the front and one in the rear. Two sets of tires equal two axles.
-- INSERT INTO Truck VALUES ('{vin}', '{cargo_capacity}', '{cargo_cover_type}', '{no_rear_axles}');
INSERT INTO Truck VALUES ('5YJSA1CG3DFP14555', '3500', 'painted fiberglass lid', '2');
INSERT INTO Truck VALUES ('2FMZA514628322040', '2100', 'high impact plastic lid', '2');
INSERT INTO Truck VALUES ('9C2KE02007R001317', '1500', 'hard folding', '2');

-- Roof Types: textile, detachable hardtop, retractable hardtop, windblocker, safety
-- INSERT INTO Convertible VALUES ('{vin}', '{back_seat_count}', '{roof_type}');
INSERT INTO Convertible VALUES ('JM2UF2138N0251579', '0', 'windblocker');
INSERT INTO Convertible VALUES ('WP0CB2961NS702088', '0', 'retractable hardtop');
INSERT INTO Convertible VALUES ('JTHBP5C23D5010933', '0', 'retractable hardtop');

-- INSERT INTO Car VALUES ('{vin}', '{number_of_doors}');
INSERT INTO Car VALUES ('KM8SG13D27U108692', '4');
INSERT INTO Car VALUES ('JHMBE376055202903', '4');
INSERT INTO Car VALUES ('5J8TB4H30DL000860', '4');

-- INSERT INTO Vehicle-Color VALUES ('{vin}', '{color}');
INSERT INTO Vehicle_Color VALUES ('5TFET54117X016058', 'Blue');
INSERT INTO Vehicle_Color VALUES ('5TFET54117X016058', 'White');
INSERT INTO Vehicle_Color VALUES ('2T1BR30E273767487', 'Black');
INSERT INTO Vehicle_Color VALUES ('JM1GC2210E1604771', 'Blue');
INSERT INTO Vehicle_Color VALUES ('YV2A4B1C5VA264304', 'White');
INSERT INTO Vehicle_Color VALUES ('WBAAF9310MEE65124', 'Black');
INSERT INTO Vehicle_Color VALUES ('3G1JD5SH0E0013280', 'White');
INSERT INTO Vehicle_Color VALUES ('4TAWN74N2YZ581143', 'White');
INSERT INTO Vehicle_Color VALUES ('1N6SD16Y2MC404130', 'White');
INSERT INTO Vehicle_Color VALUES ('5YJSA1CG3DFP14555', 'Metallic');
INSERT INTO Vehicle_Color VALUES ('2FMZA514628322040', 'Red');
INSERT INTO Vehicle_Color VALUES ('9C2KE02007R001317', 'Black');
INSERT INTO Vehicle_Color VALUES ('JM2UF2138N0251579', 'White');
INSERT INTO Vehicle_Color VALUES ('JM2UF2138N0251579', 'Black');
INSERT INTO Vehicle_Color VALUES ('WP0CB2961NS702088', 'White');
INSERT INTO Vehicle_Color VALUES ('JTHBP5C23D5010933', 'Black');
INSERT INTO Vehicle_Color VALUES ('KM8SG13D27U108692', 'Grey');
INSERT INTO Vehicle_Color VALUES ('JHMBE376055202903', 'Red');
INSERT INTO Vehicle_Color VALUES ('5J8TB4H30DL000860', 'Red');

-- INSERT INTO Customer VALUES ('{id}', '{address}', '{phone_number}', '{email_address}');
-- Individuals
INSERT INTO Customer VALUES ('D123-456-07-898-7', '4088 Geoffrey Corners Apt. 792, New Rogerstad, MA 33464', '+1(541)530-1393', 'mariasanchez@gmail.com');
INSERT INTO Customer VALUES ('R134-784-98-536-0', '55595 Dominique Centers Apt. 697, Lake Charlesland, IA 27299', '+1(676)157-2367', 'jdunn@yahoo.com');
INSERT INTO Customer VALUES ('Z876-033-433-665-2', '110 Tiffany Shoals, New Sherrybury, TN 65147', '+1(709)193-9285', 'chrisb@outlook.com');
INSERT INTO Customer VALUES ('P773-435-222-468-1', '30021 David Isle, North Gabrielmouth, AZ 29370', '+1(462)787-6488', 'agraham@outlook.com');
INSERT INTO Customer VALUES ('L833-772-834-343-9', '43977 Phillip Inlet Apt. 495, Robinsonstad, NH 71856', '+1(970)483-4219', 'whitneyreyes@gmail.com');
-- Businesses
INSERT INTO Customer VALUES ('252-61-9022', '563 Michael Unions Apt. 933, North Richard, AZ 04679', '+1(476)979-0393', 'thomas@thofix.com');
INSERT INTO Customer VALUES ('386-61-8197', '62879 Martin Expressway, Austinfort, NJ 74217', '+1(446)289-3440', 'tjackson2@lach.com');
INSERT INTO Customer VALUES ('896-45-6688', '876 Jimenez Branch Apt. 567, South Alishaville, CO 60245', '+1(660)064-4266', 'jdelgado5@wemove.com');
INSERT INTO Customer VALUES ('116-91-2450', '27403 Hannah Pass, Cabreraburgh, NH 91563', '+1(988)842-1875', 'melissa.fox@jzgroup.com');
INSERT INTO Customer VALUES ('869-87-9830', '56701 Valencia Street Suite 507, Juliaside, MS 65580', '+1(926)511-5793', 'sharon.buckley@wsons.com');

-- INSERT INTO Individual VALUES ('{driver_license_number}', '{firstname}', '{lastname}');
INSERT INTO Individual VALUES ('D123-456-07-898-7', 'Maria', 'Sanchez');
INSERT INTO Individual VALUES ('R134-784-98-536-0', 'James', 'Dunn');
INSERT INTO Individual VALUES ('Z876-033-433-665-2', 'Christopher', 'Beasley');
INSERT INTO Individual VALUES ('P773-435-222-468-1', 'Aimee', 'Graham');
INSERT INTO Individual VALUES ('L833-772-834-343-9', 'Whitney', 'Reyes');

-- INSERT INTO Business VALUES ('{tin}', '{business_name}', '{primary_contact_name}', '{primary_contact_title}');
INSERT INTO Business VALUES ('252-61-9022', 'Thomas Fixes Ltd', 'Thomas Kelly', 'CEO');
INSERT INTO Business VALUES ('386-61-8197', 'Lopez Air Conditioning and Heating', 'Tyler Jackson', 'Purchasing Department');
INSERT INTO Business VALUES ('896-45-6688', 'WeMove Inc', 'Jessica Delgado', 'Manager');
INSERT INTO Business VALUES ('116-91-2450', 'Jenkins-Zuniga Group', 'Melissa Fox', 'Buyer');
INSERT INTO Business VALUES ('869-87-9830', 'Wood and Sons Ltd', 'Sharon Buckley', 'General Manager');

-- INSERT INTO Vehicle_Sold_Customer VALUES ('{vin}', '{id}', '{sales_person_username}', '{sale_date}', '{sold_price}');
INSERT INTO Vehicle_Sold_Customer VALUES ('JM1GC2210E1604771', 'D123-456-07-898-7', 'yinan', '2021-04-25', '28600');
INSERT INTO Vehicle_Sold_Customer VALUES ('2FMZA514628322040', 'R134-784-98-536-0', 'rolan', '2021-06-29', '28700');
INSERT INTO Vehicle_Sold_Customer VALUES ('JM2UF2138N0251579', 'L833-772-834-343-9', 'leo', '2021-09-25', '33600');
INSERT INTO Vehicle_Sold_Customer VALUES ('5J8TB4H30DL000860', 'L833-772-834-343-9', 'leo', '2021-09-25', '40100');
INSERT INTO Vehicle_Sold_Customer VALUES ('KM8SG13D27U108692', '116-91-2450', 'yinan', '2021-06-26', '25600');
INSERT INTO Vehicle_Sold_Customer VALUES ('3G1JD5SH0E0013280', '896-45-6688', 'leo', '2021-07-22', '38000');
INSERT INTO Vehicle_Sold_Customer VALUES ('4TAWN74N2YZ581143', '896-45-6688', 'leo', '2021-07-22', '29600');
INSERT INTO Vehicle_Sold_Customer VALUES ('9C2KE02007R001317', '869-87-9830', 'yinan', '2021-09-23', '45600');
INSERT INTO Vehicle_Sold_Customer VALUES ('JHMBE376055202903', '252-61-9022', 'yinan', '2021-05-02', '31200');

-- INSERT INTO Repair VALUES ('{vin}', '{customer_id}', '{start_date}', '{service_writer_username}', '{repair_description}', '{completion_date}', '{odometer_reading}', '{labor_charges}');
INSERT INTO Repair 
VALUES ('4TAWN74N2YZ581143', '896-45-6688', '2021-08-22', 'ding', 'patch flat tire', '2021-08-22', '28563', '30');
INSERT INTO Repair 
VALUES ('2FMZA514628322040', 'R134-784-98-536-0', '2021-10-11', 'ding', 'oil leaking', '2021-10-11', '23607', '30');
INSERT INTO Repair 
VALUES ('2FMZA514628322040', 'R134-784-98-536-0', '2021-10-23', 'ding', 'oil leaking', '2021-10-24', '23807', '50');
INSERT INTO Repair 
VALUES ('9C2KE02007R001317', '869-87-9830', '2021-11-13', 'ding', 'Bent rear bumper', NULL, '19562', '70');
INSERT INTO Repair 
VALUES ('JHMBE376055202903', '252-61-9022', '2021-11-12', 'ding', 'Bent door', NULL, '22933', '150');

-- INSERT INTO Part VALUES ('{vin}', '{customer_id}', '{start_date}', '{part_number}', '{vendor_name}', '{quantity}', '{price}');
INSERT INTO Part VALUES ('2FMZA514628322040', 'R134-784-98-536-0', '2021-10-23', '0ilhose', 'Autozone', '2', '24.5');
INSERT INTO Part VALUES ('9C2KE02007R001317', '869-87-9830', '2021-11-13', 'Re4rBumper', 'LKQ Pick Your Part', '1', '58.75');
INSERT INTO Part VALUES ('JHMBE376055202903', '252-61-9022', '2021-11-12', 'D00r', 'LKQ Pick Your Part', '1', '350');

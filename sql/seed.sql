SELECT * FROM "Environment";


SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'Profile';

SELECT * FROM "EnvUser";

-- Create Users
INSERT INTO "User" (role, "createdAt", "lastLogin", email, password)
VALUES
    ( 'normal', '2025-06-16', '2025-06-15', 'admin@example.com', 'securepassword1'),
    ('normal', '2025-06-16', NULL, 'user@example.com', 'securepassword2');

-- Create Environments
INSERT INTO "Environment" ( cords, "createdAt", scale, name, address, "pathCartographie")
VALUES
    ('{"lat": 40.7128, "lng": -74.0060}', '2025-06-16', 1, 'Environment 1', '123 Main St', '/path/to/cartography1'),
    ('{"lat": 34.0522, "lng": -118.2437}', '2025-06-16', 2, 'Environment 2', '456 Elm St', '/path/to/cartography2');

-- Create EndUser Relationships
INSERT INTO "EnvUser" ("userId", "envId")
VALUES
    (14, 1),
    ( 15, 2);

    -- Create Profiles for Users 14 and 15
    INSERT INTO "Profile" ("userId", "firstname", "lastname", "address","phonenumber")
    VALUES
        (14, 'Admin', 'User', 'Algiers, Algeria', '1234567890'),
        (15, 'Normal', 'User', 'Algiers, Algeria', '0987654321');

    SELECT * FROM information_schema.key_column_usage WHERE table_name = 'EnvUser';


INSERT INTO "Device" ("type", "status", "price", "createdAt", "userId", "cpuUsage","macAddress", "ramUsage") 
VALUES
    ('sensor', 'connected', 100.00, '2025-05-16', 14, 30.5, 'E4:5F:01:08:18:C8', 2048),


    SELECT
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

SELECT * from "Environment";
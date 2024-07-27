-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT * FROM crime_scene_reports WHERE year = 2023 AND month = 7 AND day = 28 AND street LIKE '
%Humphrey Street%'; -- userfull info 10:15

SELECT * FROM interviews WHERE year = 2023 AND month = 7 AND day = 28;

-- names of caller and receiver
SELECT pc.id, pc.year, pc.month, pc.day, caller.name AS caller_name, receiver.name AS receiver_name, pc.duration
FROM phone_calls AS pc
JOIN people AS caller ON pc.caller = caller.phone_number
JOIN people AS receiver ON pc.receiver = receiver.phone_number
WHERE pc.year = 2023  AND pc.month = 7 AND pc.day = 28
AND pc.duration < 60;

-- Starting suspecteds
--+-----+------+-------+-----+-------------+---------------+----------+
--| id  | year | month | day | caller_name | receiver_name | duration |
--+-----+------+-------+-----+-------------+---------------+----------+
--| 221 | 2023 | 7     | 28  | Sofia       | Jack          | 51       |
--| 224 | 2023 | 7     | 28  | Kelsey      | Larry         | 36       |
--| 233 | 2023 | 7     | 28  | Bruce       | Robin         | 45       | (*)
--| 251 | 2023 | 7     | 28  | Kelsey      | Melissa       | 50       |
--| 254 | 2023 | 7     | 28  | Taylor      | James         | 43       |
--| 255 | 2023 | 7     | 28  | Diana       | Philip        | 49       |
--| 261 | 2023 | 7     | 28  | Carina      | Jacqueline    | 38       |
--| 279 | 2023 | 7     | 28  | Kenny       | Doris         | 55       |
--| 281 | 2023 | 7     | 28  | Benista     | Anna          | 54       |
--+-----+------+-------+-----+-------------+---------------+----------+

-- names of atm transaction user
SELECT atm.account_number, atm.amount, p.name
FROM atm_transactions AS atm
JOIN bank_accounts AS ba ON atm.account_number = ba.account_number
JOIN people AS p ON ba.person_id = p.id
WHERE atm.year = 2023 AND atm.month = 7 AND atm.day = 28
    AND atm.atm_location = 'Leggett Street'
    AND atm.transaction_type = 'withdraw';
--
--+----------------+--------+---------+
--| account_number | amount |  name   |
--+----------------+--------+---------+
--| 49610011       | 50     | Bruce   | X
--| 26013199       | 35     | Diana   | X
--| 16153065       | 80     | Brooke  |
--| 28296815       | 20     | Kenny   |
--| 25506511       | 20     | Iman    |
--| 28500762       | 48     | Luca    |
--| 76054385       | 60     | Taylor  | X
--| 81061156       | 30     | Benista | X
--+----------------+--------+---------+

-- now i want to go deep on how took the first flight in the morning, so i would like to identify the first flight:
WITH Fiftyville_Airports AS(
    SELECT id AS origin_id    FROM airports    WHERE city = 'Fiftyville')
    SELECT a.abbreviation, a.full_name, a.city, f.id, a2.full_name AS destination_city, f.hour, f.minute FROM airports AS a
    JOIN flights AS f ON a.id = f.origin_airport_id JOIN airports AS a2 ON f.destination_airport_id = a2.id
    JOIN Fiftyville_Airports AS fa ON f.origin_airport_i d = fa.origin_id WHERE f.year = 2023 AND f.month = 7 AND f.day = 29
    ORDER BY f.hour, f.minute;

-- | CSF          | Fiftyville Regional Airport | Fiftyville | 36 | LaGuardia Airport                   | 8    | 20     |

-- I want know the city associated at LGA Airport
SELECT city FROM airports WHERE abbreviation = 'LGA' OR full_name LIKE '%LaGuardia%';

--+---------------+
--|     city      |
--+---------------+
--| New York City |
--+---------------+

SELECT DISTINCT p.name AS passenger_name FROM passengers AS ps JOIN flights AS f ON ps.flight_id = f.id JOIN airports AS a
ON f.destination_airport_id = a.id JOIN people AS p ON ps.passport_number = p.passport_number WHERE a.abbreviation = 'LGA';

--+----------------+
--| passenger_name |
--+----------------+
--| Philip         |
--| Jason          |
--| Gerald         |
--| Lauren         |
--| Carl           |
--| James          |
--| Arthur         |
--| Brooke         |
--| Larry          |
--| Steven         |
--| John           |
--| Pamela         |
--| Melissa        |
--| Sharon         |
--| Olivia         |
--| Jean           |
--| Judith         |
--| Natalie        |
--| Laura          |
--| Paul           |
--| Sean           |
--| Nancy          |
--| Doris          |
--| Sofia          |
--| Bruce          | X
--| Edward         |
--| Kelsey         |
--| Taylor         | X
--| Kenny          |
--| Luca           |
--| Ernest         |
--| Jeffrey        |
--| Brenda         |
--| Jerry          |
--| Barbara        |
--| Eugene         |
--+----------------+

SELECT p.name, bsl.hour, bsl.minute FROM bakery_security_logs AS bsl JOIN people AS p ON p.license_plate = bsl.license_plate WHERE bsl.year = 2023  AND bsl.month = 7  AND bsl.day = 28  AND bsl.activity = 'exit'   AND bsl.hour = 10  AND bsl.minute BETWEEN 15 AND 25 ORDER BY bsl.minute;
--+---------+------+--------+
--|  name   | hour | minute |
--+---------+------+--------+
--| Vanessa | 10   | 16     |
--| Bruce   | 10   | 18     | X <-- Bruce is the criminal!
--| Barry   | 10   | 18     |
--| Luca    | 10   | 19     |
--| Sofia   | 10   | 20     |
--| Iman    | 10   | 21     |
--| Diana   | 10   | 23     |
--| Kelsey  | 10   | 23     |
--+---------+------+--------+

-- The THIEF is: Bruce
-- The city the thief ESCAPED TO: New York
-- The ACCOMPLICE is: Robin ( Cause phone call (*) )




CREATE VIEW partner_info AS 
SELECT F.photo_url AS Photo, F.name AS Name, F.research_interest AS Research_Interest,
        U.name AS University, F.position AS Position, F.email AS Email, F.phone AS Phone
FROM faculty F, university U
WHERE F.university_id = U.id




ALTER TABLE faculty_keyword ADD CONSTRAINT fk_keyword FOREIGN KEY (keyword_id) REFERENCES keyword (id);



ALTER TABLE keyword ADD INDEX idx_keyword_name (name);

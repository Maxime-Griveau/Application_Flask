CREATE TABLE courseau (
    id SERIAL PRIMARY KEY,
    denomination TEXT(45) UNIQUE NOT NULL,
    longueur INTEGER,
    type_id INTEGER,
    derniere_crue_majeure DATE,
    est_affluent BOOLEAN NOT NULL,
    FOREIGN KEY (type_id) REFERENCES typecourseau (id)
);

CREATE TABLE traverse (
    courseau_id VARCHAR(10),
    sousdivision_geographique_id VARCHAR(10),
    PRIMARY KEY (courseau_id, sousdivision_geographique_id),
    FOREIGN KEY (courseau_id) REFERENCES courseau (id),
    FOREIGN KEY (sousdivision_geographique_id) REFERENCES sousdivision_geographique (id)
);

CREATE TABLE typecourseau (
    id SERIAL PRIMARY KEY,
    label VARCHAR(45) NOT NULL,
    commentaire TEXT
);

CREATE TABLE sousdivision_geographique (
    id SERIAL PRIMARY KEY,
    pays_id INTEGER,
    type_id INTEGER,
    denomination VARCHAR(45) NOT NULL,
    code_officiel VARCHAR(12),
    FOREIGN KEY (pays_id) REFERENCES pays (id),
    FOREIGN KEY (type_id) REFERENCES typesousdivision (id)
);

CREATE TABLE typesousdivision (
    id SERIAL PRIMARY KEY,
    label VARCHAR(45) NOT NULL,
    commentaire TEXT
);

CREATE TABLE pays (
    id SERIAL PRIMARY KEY,
    denomination VARCHAR(45) NOT NULL
);

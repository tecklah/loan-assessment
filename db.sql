CREATE TABLE public.customer_account_status (
	id int4 NOT NULL,
	"name" varchar(200) NOT NULL,
	nationality varchar(200) NOT NULL,
	email varchar(200) NOT NULL,
	account_status varchar(200) NOT NULL,
	CONSTRAINT customer_account_status_pk PRIMARY KEY (id)
);

INSERT INTO public.customer_account_status
(id, "name", nationality, email, account_status)
VALUES(1111, 'Loren', 'Singaporean', 'loren@gmail.com', 'good-standing');
INSERT INTO public.customer_account_status
(id, "name", nationality, email, account_status)
VALUES(2222, 'Matt', 'Non-Singaporean', 'matt@yahoo.com', 'closed');
INSERT INTO public.customer_account_status
(id, "name", nationality, email, account_status)
VALUES(3333, 'Hilda', 'Singaporean', 'halida@gmail.com', 'delinquent');
INSERT INTO public.customer_account_status
(id, "name", nationality, email, account_status)
VALUES(4444, 'Andy', 'Non-Singaporean', 'andy@gmail.com', 'good-standing');
INSERT INTO public.customer_account_status
(id, "name", nationality, email, account_status)
VALUES(5555, 'Kit', 'Singaporean', 'kit@yahho.com', 'delinquent');

CREATE TABLE public.customer_credit_score (
	id int4 NOT NULL,
  "name" varchar(200) NOT NULL,
  email varchar(200) NOT NULL,
  credit_score int NOT NULL,
	CONSTRAINT customer_credit_score_pk PRIMARY KEY (id)
);

INSERT INTO customer_credit_score
(id, name, email, credit_score)
VALUES(1111, 'Loren', 'loren@gmail.com', 455);
INSERT INTO customer_credit_score
(id, name, email, credit_score)
VALUES(2222, 'Matt', 'matt@yahoo.com', 685);
INSERT INTO customer_credit_score
(id, name, email, credit_score)
VALUES(3333, 'Hilda', 'halida@gmail.com', 825);
INSERT INTO customer_credit_score
(id, name, email, credit_score)
VALUES(4444, 'Andy', 'andy@gmail.com', 840);
INSERT INTO customer_credit_score
(id, name, email, credit_score)
VALUES(5555, 'Kit', 'kit@yahho.com', 350);

CREATE TABLE public.government_pr_status (
  id int4 NOT NULL,
  "name" varchar(200) NOT NULL,
  email varchar(200) NOT NULL,
  pr_status varchar(200) NOT NULL,
	CONSTRAINT government_pr_status_pk PRIMARY KEY (id)
);

INSERT INTO government_pr_status
(id, name, email, pr_status)
VALUES(2222, 'Matt', 'matt@yahoo.com', 'true');
INSERT INTO government_pr_status
(id, name, email, pr_status)
VALUES(4444, 'Andy', 'andy@gmail.com', 'false');
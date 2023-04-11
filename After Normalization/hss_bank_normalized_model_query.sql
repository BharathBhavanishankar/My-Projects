-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema hss_bank
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `hss_bank` ;

-- -----------------------------------------------------
-- Schema hss_bank
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `hss_bank` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `hss_bank` ;

-- -----------------------------------------------------
-- Table `bank_customer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bank_customer` ;

CREATE TABLE IF NOT EXISTS `bank_customer` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `first_anme` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `date_of_birth` DATE NOT NULL,
  PRIMARY KEY (`customer_id`))
ENGINE = InnoDB
COMMENT = 'Has details about bank customer id and name';


-- -----------------------------------------------------
-- Table `bank_branch`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bank_branch` ;

CREATE TABLE IF NOT EXISTS `bank_branch` (
  `branch_id` INT NOT NULL AUTO_INCREMENT,
  `branch_name` VARCHAR(50) NOT NULL,
  `branch_address` VARCHAR(255) NOT NULL,
  `city` VARCHAR(50) NOT NULL,
  `state` VARCHAR(50) NOT NULL,
  `zip_code` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`branch_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'Has details about different branches of hss bank';


-- -----------------------------------------------------
-- Table `account_details`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `account_details` ;

CREATE TABLE IF NOT EXISTS `account_details` (
  `account_number` INT NOT NULL AUTO_INCREMENT,
  `branch_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `account_type` ENUM('savings', 'salary') NOT NULL,
  `account_status` ENUM('active', 'inactive') NOT NULL,
  `account_balance` DECIMAL(10,2) NULL DEFAULT NULL,
  `account_start_date` DATE NOT NULL,
  `account_end_date` DATE NULL DEFAULT NULL,
  `balance` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`account_number`),
  INDEX `fk_account_details_bank_customer1_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_account_details_bank_branch1_idx` (`branch_id` ASC) VISIBLE,
  CONSTRAINT `fk_account_details_bank_customer1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `bank_customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_account_details_bank_branch1`
    FOREIGN KEY (`branch_id`)
    REFERENCES `bank_branch` (`branch_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'Has details about customer account';

-- -----------------------------------------------------
-- Adding constraint manually to table account detail
-- -----------------------------------------------------

RENAME TABLE account_details to account_detail;
ALTER TABLE account_detail
ADD CONSTRAINT account_end_date_ck1 
CHECK (
(account_status = 'inactive' AND account_end_date IS NOT NULL) OR 
(account_status = 'active' AND account_end_date IS NULL)
);
 
 
 -- -----------------------------------------------------
-- calculation for current account balance
-- -----------------------------------------------------
SELECT ad.account_number, atr.transaction_date, atr.transaction_type, atr.transaction_amount, COALESCE(ad.account_balance + SUM(atr.transaction_amount AND atr.transaction_type = 'deposit') - SUM(atr.transaction_amount AND transaction_type = 'withdraw')) AS balance
FROM account_detail ad 
JOIN account_transaction atr ON atr.account_number = ad.account_number
GROUP BY ad.account_number;
 
-- -----------------------------------------------------
-- Table `loan_info`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `loan_info` ;

CREATE TABLE IF NOT EXISTS `loan_info` (
  `loan_id` INT NOT NULL AUTO_INCREMENT,
  `account_number` INT NOT NULL,
  `loan_type` ENUM('personal_loan', 'business_loan') NOT NULL,
  `loan_amount` DECIMAL(15,2) NULL DEFAULT NULL,
  `loan_issue_date` DATE NOT NULL,
  `interest_rate` DECIMAL(5,2) NOT NULL,
  `loan_closure_date` DATE NOT NULL,
  PRIMARY KEY (`loan_id`),
  INDEX `fk_loan_info_account_details1_idx` (`account_number` ASC) VISIBLE,
  CONSTRAINT `fk_loan_info_account_details1`
    FOREIGN KEY (`account_number`)
    REFERENCES `account_details` (`account_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'Has detail about loan lended to customers';


-- -----------------------------------------------------
-- Table `transaction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `transaction` ;

CREATE TABLE IF NOT EXISTS `transaction` (
  `transaction_id` INT NOT NULL AUTO_INCREMENT,
  `account_number` INT NOT NULL,
  `transaction_mode` ENUM('net_banking', 'cheque', 'upi') NOT NULL,
  `transaction_date` DATETIME NOT NULL,
  `transaction_type` ENUM('debit', 'withdraw') NOT NULL,
  `transaction_amount` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`transaction_id`),
  INDEX `account_number` (`account_number` ASC) VISIBLE,
  CONSTRAINT `transaction_ibfk_1`
    FOREIGN KEY (`account_number`)
    REFERENCES `account_details` (`account_number`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'Has transaction history of all accounts';

RENAME TABLE transaction TO account_transaction;

-- -----------------------------------------------------------------------------------
-- manually setting constraint to check the min and max transaction that can be done
-- -----------------------------------------------------------------------------------

ALTER TABLE account_transaction
ADD CONSTRAINT transaction_amount_ck1
CHECK (
transaction_amount >= 100 AND transaction_amount <= 50000
);


-- -----------------------------------------------------
-- Table `bank_employee`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bank_employee` ;

CREATE TABLE IF NOT EXISTS `bank_employee` (
  `employee_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `date_of_birth` DATE NOT NULL,
  `supervisor_id` INT NULL,
  PRIMARY KEY (`employee_id`),
  INDEX `fk_bank_employee_bank_employee2_idx` (`supervisor_id` ASC) VISIBLE,
  CONSTRAINT `fk_bank_employee_bank_employee2`
    FOREIGN KEY (`supervisor_id`)
    REFERENCES `bank_employee` (`employee_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'Has details about bank employee id and name';


-- -----------------------------------------------------
-- Table `employee_designation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `employee_designation` ;

CREATE TABLE IF NOT EXISTS `employee_designation` (
  `designation_id` INT NOT NULL AUTO_INCREMENT,
  `designation_name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`designation_id`))
ENGINE = InnoDB
COMMENT = 'This table has information about employee designations available in this bank';


-- -----------------------------------------------------
-- Table `bank_employee_detail`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bank_employee_detail` ;

CREATE TABLE IF NOT EXISTS `bank_employee_detail` (
  `employee_id` INT NOT NULL,
  `designation_id` INT NOT NULL,
  `branch_id` INT NOT NULL,
  `employee_hire` DATE NOT NULL,
  `employment_type` ENUM('permanent', 'contract') NOT NULL,
  `employee_left` DATE NULL,
  `phone_number` VARCHAR(15) NOT NULL,
  `employee_address` VARCHAR(255) NOT NULL,
  `city` VARCHAR(50) NOT NULL,
  `state` VARCHAR(50) NOT NULL,
  `zip_code` VARCHAR(10) NOT NULL,
  `mail_id` VARCHAR(25) NOT NULL,
  `latest_update` DATE NOT NULL,
  INDEX `fk_bank_employee_history_bank_employee1_idx` (`employee_id` ASC) VISIBLE,
  UNIQUE INDEX `mail_id_UNIQUE` (`mail_id` ASC) VISIBLE,
  INDEX `fk_bank_employee_history_bank_branch2_idx` (`branch_id` ASC) VISIBLE,
  INDEX `fk_bank_employee_details_employee_designation1_idx` (`designation_id` ASC) VISIBLE,
  CONSTRAINT `fk_bank_employee_history_bank_employee1`
    FOREIGN KEY (`employee_id`)
    REFERENCES `bank_employee` (`employee_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bank_employee_history_bank_branch2`
    FOREIGN KEY (`branch_id`)
    REFERENCES `bank_branch` (`branch_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bank_employee_details_employee_designation1`
    FOREIGN KEY (`designation_id`)
    REFERENCES `employee_designation` (`designation_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'This table has details about history of employees served for hss bank';


-- -----------------------------------------------------
-- Table `customer_designation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `customer_designation` ;

CREATE TABLE IF NOT EXISTS `customer_designation` (
  `designation_id` INT NOT NULL,
  `designation_name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`designation_id`))
ENGINE = InnoDB
COMMENT = 'This table has information about customer designations';


-- -----------------------------------------------------
-- Table `bank_customer_detail`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bank_customer_detail` ;

CREATE TABLE IF NOT EXISTS `bank_customer_detail` (
  `customer_id` INT NOT NULL,
  `designation_id` INT NOT NULL,
  `salary` DECIMAL(15,2) NOT NULL,
  `company_name` VARCHAR(50) NOT NULL,
  `customer_mail_id` VARCHAR(100) NOT NULL,
  `phone_number` VARCHAR(15) NOT NULL,
  `customer_address` VARCHAR(255) NOT NULL,
  `city` VARCHAR(50) NOT NULL,
  `state` VARCHAR(50) NOT NULL,
  `zip_code` VARCHAR(10) NOT NULL,
  `latest_update` DATE NOT NULL,
  INDEX `fk_bank_customer_history_bank_customer1_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_bank_customer_detail_customer_designation1_idx` (`designation_id` ASC) VISIBLE,
  CONSTRAINT `fk_bank_customer_history_bank_customer1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `bank_customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bank_customer_detail_customer_designation1`
    FOREIGN KEY (`designation_id`)
    REFERENCES `customer_designation` (`designation_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'This table has all customer detail';


-- -----------------------------------------------------
-- Table `loan_transaction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `loan_transaction` ;

CREATE TABLE IF NOT EXISTS `loan_transaction` (
  `loan_id` INT NOT NULL,
  `loan_due_paid_date` DATE NOT NULL,
  `loan_paid_amount` DECIMAL(10,2),
  `next_due_date` DATE NOT NULL,
  `next_due_amount` DECIMAL(15,2) NOT NULL,
  `loan_balance` DECIMAL(15,2),
  INDEX `fk_loan_transaction_loan_info1_idx` (`loan_id` ASC) VISIBLE,
  CONSTRAINT `fk_loan_transaction_loan_info1`
    FOREIGN KEY (`loan_id`)
    REFERENCES `loan_info` (`loan_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'This table has details about customer account loan payment';

-- ------------------------------------------------------
-- manually writing query for getting balance to be paid
-- ------------------------------------------------------

SELECT li.loan_id, COALESCE(li.loan_amount - SUM(lt.loan_paid_amount)) AS loan_balance_amount
FROM loan_info li JOIN loan_transaction lt ON li.loan_id = lt.loan_id
GROUP BY lt.loan_id;

-- --------------------------------------------------------------------
-- manually writing query for getting next due amount and next due date
-- --------------------------------------------------------------------

SELECT li.loan_id, lt.next_due_date, COALESCE(li.loan_amount - SUM(lt.loan_paid_amount)) / (TIMESTAMPDIFF(MONTH, li.loan_issue_date, lt.loan_due_paid_date)*li.interest_rate) AS next_due_amount
FROM loan_info li JOIN loan_transaction lt ON li.loan_id = lt.loan_id
WHERE lt.next_due_date = lt.loan_due_paid_date + 30
GROUP BY lt.loan_id
ORDER BY lt.loan_due_paid_date, lt.loan_due_paid_date DESC
LIMIT 1;

-- -----------------------------------------------------
-- Table `deposit`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `deposit` ;

CREATE TABLE IF NOT EXISTS `deposit` (
  `deposit_id` INT NOT NULL,
  `account_number` INT NOT NULL,
  `deposit_type` ENUM('fixed', 'recurring') NOT NULL,
  `deposit_period` INT NOT NULL,
  PRIMARY KEY (`deposit_id`),
  INDEX `fk_deposit_account_details2_idx` (`account_number` ASC) VISIBLE,
  CONSTRAINT `fk_deposit_account_details2`
    FOREIGN KEY (`account_number`)
    REFERENCES `account_details` (`account_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'Has detail about accounts and its deposit';


-- -----------------------------------------------------
-- Table `deposits_history`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `deposits_history` ;

CREATE TABLE IF NOT EXISTS `deposits_history` (
  `deposit_id` INT NOT NULL,
  `deposit_amount` DECIMAL(15,2) NOT NULL,
  `deposit_date` DATE NOT NULL,
  `deposit_status` ENUM('active', 'closed') NOT NULL,
  `deposit_closed_date` DATE NULL,
  INDEX `fk_deposits_history_deposit1_idx` (`deposit_id` ASC) VISIBLE,
  CONSTRAINT `fk_deposits_history_deposit1`
    FOREIGN KEY (`deposit_id`)
    REFERENCES `deposit` (`deposit_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'This table has details about customer account deposit transaction';

RENAME TABLE deposits_history to deposit_history;

-- ---------------------------------------------------------
-- Manually adding constraint for deposit closed date column
-- ---------------------------------------------------------

ALTER TABLE deposit_history
ADD CONSTRAINT deposit_closed_date_ck1
CHECK
(
(deposit_status = 'active' AND deposit_closed_date IS NULL) OR
(deposit_status = 'inactive' AND deposit_closed_date IS NOT NULL)
);

-- -----------------------------------------------------
-- Table `contract_employee`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `contract_employee` ;

CREATE TABLE IF NOT EXISTS `contract_employee` (
  `contract_id` INT NOT NULL AUTO_INCREMENT,
  `contract_start` DATE NOT NULL,
  `contract_end` DATE NOT NULL,
  `employee_id` INT NOT NULL,
  PRIMARY KEY (`contract_id`),
  INDEX `fk_contract_employee_bank_employee1_idx` (`employee_id` ASC) VISIBLE,
  CONSTRAINT `fk_contract_employee_bank_employee1`
    FOREIGN KEY (`employee_id`)
    REFERENCES `bank_employee` (`employee_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'This table has information about contract employee';


 -- ----------------------------------------------------------------------------------------------------------------------------
-- setting condition for employee id in contract employee table where employment type in bank employee detail table is contract
-- -----------------------------------------------------------------------------------------------------------------------------

 INSERT INTO contract_employee (employee_id)
 SELECT employee_id FROM bank_employee_detail WHERE employment_type = 'contract';

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

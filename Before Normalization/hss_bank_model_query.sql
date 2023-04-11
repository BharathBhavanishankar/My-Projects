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

-- -----------------------------------------------------
-- Schema hss_bank
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `hss_bank` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `hss_bank` ;

-- -----------------------------------------------------
-- Table `hss_bank`.`bank_branch`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hss_bank`.`bank_branch` (
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
-- Table `hss_bank`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hss_bank`.`customer` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `date_of_birth` DATE NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `phone_number` VARCHAR(15) NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  `city` VARCHAR(50) NOT NULL,
  `state` VARCHAR(50) NOT NULL,
  `zip_code` VARCHAR(10) NOT NULL,
  `branch_id` INT NOT NULL,
  `loan` ENUM('yes', 'no') NOT NULL,
  `customer_designation` VARCHAR(15) NOT NULL,
  `salary` DECIMAL(15,2) NOT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE INDEX `email` (`email` ASC),
  UNIQUE INDEX `phone_number` (`phone_number` ASC),
  INDEX `branch_id` (`branch_id` ASC),
  CONSTRAINT `customer_ibfk_1`
    FOREIGN KEY (`branch_id`)
    REFERENCES `hss_bank`.`bank_branch` (`branch_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'Has details about customers of hss bank';


-- -----------------------------------------------------
-- Table `hss_bank`.`account_details`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hss_bank`.`account_details` (
  `account_number` INT NOT NULL AUTO_INCREMENT,
  `account_type` ENUM('savings', 'salary') NOT NULL,
  `account_status` ENUM('active', 'inactive') NOT NULL,
  `account_start_date` DATE NOT NULL,
  `account_end_date` DATE NULL,
  `balance` DECIMAL(10,2) NOT NULL,
  `customer_id` INT NOT NULL,
  PRIMARY KEY (`account_number`),
  INDEX `customer_id` (`customer_id` ASC),
  CONSTRAINT `account_type_ibfk_1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `hss_bank`.`customer` (`customer_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'Has details about customer account';



-- -----------------------------------------------------
-- Table `hss_bank`.`bank_branch_manager`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hss_bank`.`bank_branch_manager` (
  `manager_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `phone_number` VARCHAR(15) NOT NULL,
  `branch_id` INT NOT NULL,
  PRIMARY KEY (`manager_id`),
  UNIQUE INDEX `email` (`email` ASC),
  UNIQUE INDEX `phone_number` (`phone_number` ASC),
  INDEX `branch_id` (`branch_id` ASC),
  CONSTRAINT `bank_branch_manager_ibfk_1`
    FOREIGN KEY (`branch_id`)
    REFERENCES `hss_bank`.`bank_branch` (`branch_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'Has details about managers of different branches of hss bank';


-- -----------------------------------------------------
-- Table `hss_bank`.`bank_employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hss_bank`.`bank_employee` (
  `employee_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `employment_type` ENUM('permanent', 'contract') NOT NULL,
  `designation` VARCHAR(45) NOT NULL,
  `mail_id` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(15) NOT NULL,
  `salary` DECIMAL(15,2) NOT NULL,
  `branch_id` INT NOT NULL,
  `supervisor_id` INT NOT NULL,
  PRIMARY KEY (`employee_id`),
  INDEX `fk_bank_employee_bank_branch1_idx` (`branch_id` ASC),
  INDEX `fk_bank_employee_bank_employee1_idx` (`supervisor_id` ASC),
  CONSTRAINT `fk_bank_employee_bank_branch1`
    FOREIGN KEY (`branch_id`)
    REFERENCES `hss_bank`.`bank_branch` (`branch_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bank_employee_bank_employee1`
    FOREIGN KEY (`supervisor_id`)
    REFERENCES `hss_bank`.`bank_employee` (`employee_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'Has details about all Employees working in hss bank';

-- -----------------------------------------------------
-- Table `hss_bank`.`transaction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hss_bank`.`transaction` (
  `transaction_id` INT NOT NULL AUTO_INCREMENT,
  `transaction_mode` ENUM('net_banking', 'cheque', 'upi') NOT NULL,
  `transaction_date` DATETIME NOT NULL,
  `transaction_type` ENUM('debit', 'credit') NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  `account_number` INT NOT NULL,
  PRIMARY KEY (`transaction_id`),
  INDEX `account_number` (`account_number` ASC),
  CONSTRAINT `transaction_ibfk_1`
    FOREIGN KEY (`account_number`)
    REFERENCES `hss_bank`.`account_details` (`account_number`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = 'Has transaction history\n';

 
-- -----------------------------------------------------
-- Table `hss_bank`.`loan_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hss_bank`.`loan_info` (
  `loan_id` INT NOT NULL AUTO_INCREMENT,
  `loan_type` ENUM('personal_loan', 'business_loan') NOT NULL,
  `loan_amount` DECIMAL(15,2) NULL,
  `customer_id` INT NOT NULL,
  `loan_issued_branch_id` INT NOT NULL,
  `loan_issue_date` DATE NOT NULL,
  `interest_rate` DECIMAL(5,2) NOT NULL,
  `due_date` DATE NOT NULL,
  PRIMARY KEY (`loan_id`),
  INDEX `fk_loan_info_bank_branch1_idx` (`loan_issued_branch_id` ASC),
  INDEX `fk_loan_info_customer1_idx` (`customer_id` ASC),
  CONSTRAINT `fk_loan_info_bank_branch1`
    FOREIGN KEY (`loan_issued_branch_id`)
    REFERENCES `hss_bank`.`bank_branch` (`branch_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_loan_info_customer1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `hss_bank`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table `hss_bank`.`permanent_bank_employee`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `hss_bank`.`permanent_bank_employee` (
  `employee_id` INT NOT NULL AUTO_INCREMENT,
  `employee_hire` DATE NOT NULL,
  INDEX `fk_permanent_bank_employee_bank_employee1_idx` (`employee_id` ASC),
  CONSTRAINT `fk_permanent_bank_employee_bank_employee1`
    FOREIGN KEY (`employee_id`)
    REFERENCES `hss_bank`.`bank_employee` (`employee_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'Has details about permanent employees in hss bank';



-- -----------------------------------------------------
-- Table `hss_bank`.`contract_bank_employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hss_bank`.`contract_bank_employee` (
  `contract_id` INT NOT NULL,
  `employee_id` INT NOT NULL,
  `employee_hire` DATE NOT NULL,
  `contract_expire` DATE NOT NULL,
  PRIMARY KEY (`contract_id`),
  INDEX `fk_contract_bank_employee_bank_employee1_idx` (`employee_id` ASC),
  CONSTRAINT `fk_contract_bank_employee_bank_employee1`
    FOREIGN KEY (`employee_id`)
    REFERENCES `hss_bank`.`bank_employee` (`employee_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'Has details about contract employees in hss bank';



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

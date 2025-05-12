# Create Table & Add Constraint
    CREATE TABLE SalesPerson(
    SalesPersonID VARCHAR(5) PRIMARY KEY,
    SalesName VARCHAR(50) NOT NULL,
    DOB DATE NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Position VARCHAR(50) NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL
    );
    
    ALTER TABLE SalesPerson ADD CONSTRAINT valid_gender_salesperson CHECK (Gender IN ('Female', 'Male', 'Other'));
    ALTER TABLE SalesPerson ADD CONSTRAINT valid_position_salesperson CHECK (Position LIKE '%Chief%' OR Position LIKE '%Manager%' OR Position LIKE '%Representative%');
    ALTER TABLE SalesPerson ADD CONSTRAINT unique_phonenumber_salesperson UNIQUE (PhoneNumber);
    
    CREATE TABLE Sales(
    SalesID VARCHAR(5) PRIMARY KEY,
    SalesPersonID VARCHAR(5) NOT NULL,
    Quantity INT NOT NULL,
    Year INT NOT NULL,
    Month VARCHAR(50) NOT NULL,
    Sales INT NOT NULL,
    FOREIGN KEY (SalesPersonID) REFERENCES SalesPerson(SalesPersonID) ON UPDATE CASCADE ON DELETE CASCADE
    );
    
    ALTER TABLE Sales ADD CONSTRAINT valid_quantity_sales CHECK (Quantity > 0);
    ALTER TABLE Sales ADD CONSTRAINT valid_year_sales CHECK (Year <= DATE_PART('year', CURRENT_DATE));
    ALTER TABLE Sales ADD CONSTRAINT valide_month_sales CHECK (Month IN ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'));
    ALTER TABLE Sales ADD CONSTRAINT valid_sales_sales CHECK (Sales >= 0);
    
    CREATE TABLE KPI(
    KPI_ID VARCHAR(5) PRIMARY KEY,
    SalesPersonID VARCHAR(5) NOT NULL,
    Year INT NOT NULL,
    TargetQ INT NOT NULL,
    Quotation INT NOT NULL,
    TargetSO INT NOT NULL,
    SalesOrder INT NOT NULL,
    AllCustomer INT NOT NULL,
    CustomerInHand INT NOT NULL,
    FOREIGN KEY (SalesPersonID) REFERENCES SalesPerson(SalesPersonID) ON UPDATE CASCADE ON DELETE CASCADE
    );
    
    ALTER TABLE KPI ADD CONSTRAINT valid_year_kpi CHECK (Year <= DATE_PART('year', CURRENT_DATE));
    ALTER TABLE KPI ADD CONSTRAINT valid_targerq_kpi CHECK (TargetQ >= 0);
    ALTER TABLE KPI ADD CONSTRAINT valid_quotation_kpi CHECK (Quotation >= 0);
    ALTER TABLE KPI ADD CONSTRAINT valid_targetso_kpi CHECK (TargetSO >= 0);
    ALTER TABLE KPI ADD CONSTRAINT valid_salesorder_kpi CHECK (SalesOrder >= 0);
    ALTER TABLE KPI ADD CONSTRAINT valid_allcustomer_kpi CHECK (AllCustomer >= 0);
    ALTER TABLE KPI ADD CONSTRAINT valid_customerinhand_kpi CHECK (CustomerInHand >= 0 AND CustomerInHand <= AllCustomer);
    
    CREATE TABLE Product(
    ProductID VARCHAR(5) PRIMARY KEY,
    ProductName VARCHAR(50) NOT NULL
    InStock INT NOT NULL,
    Status VARCHAR(50) NOT NULL,
    ImportLoc VARCHAR(50) NOT NULL
    );
    
    ALTER TABLE Product ADD CONSTRAINT valid_product_status CHECK (Status IN ('Profit', 'Break-Even', 'Loss'));
    
    CREATE TABLE SalesProduct(
    SalesID VARCHAR(5) NOT NULL,
    ProductID VARCHAR(5) NOT NULL,
    TotalSales INT NOT NULL,
    TotalCost INT NOT NULL,
    Status VARCHAR(50) NOT NULL,
    PRIMARY KEY (SalesID, ProductID),
    FOREIGN KEY (SalesID) REFERENCES Sales(SalesID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
    );
    
    ALTER TABLE SalesProduct ADD CONSTRAINT valid_totalsales_salesproduct CHECK (TotalSales >= 0);
    ALTER TABLE SalesProduct ADD CONSTRAINT valid_totalcost_salesproduct CHECK (TotalCost >= 0);
    ALTER TABLE SalesProduct ADD CONSTRAINT valid_status_salesproduct CHECK (Status IN ('Pending', 'Completed', 'Cancelled'));
    
    CREATE TABLE Debtor(
    DebtorID VARCHAR(5) PRIMARY KEY,
    CompanyName VARCHAR(50) NOT NULL,
    SalesPersonID VARCHAR(5) NOT NULL,
    ProductID INT NOT NULL,
    Price INT NOT NULL,
    Debt INT NOT NULL,
    Paid INT NOT NULL,
    Date DATE NOT NULL,
    Status VARCHAR(50) NOT NULL,
    FOREIGN KEY (SalesPersonID) REFERENCES SalesPerson(SalesPersonID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON UPDATE CASCADE ON DELETE CASCADE
    );
    
    ALTER TABLE Debtor ADD CONSTRAINT valid_price_debtor CHECK (Price >= 0);
    ALTER TABLE Debtor ADD CONSTRAINT valid_debt_debtor CHECK (Debt >= 0);
    ALTER TABLE Debtor ADD CONSTRAINT valid_paid_debtor CHECK (Paid >= 0);
    ALTER TABLE Debtor ADD CONSTRAINT valid_status_debtor CHECK (Status IN ('Unpaid', 'Partially Paid', 'Paid'));
    
    CREATE TABLE Users(
      Username VARCHAR(50) PRIMARY KEY,
      SalesPersonID VARCHAR(50) NOT NULL,
      Password VARCHAR(20) NOT NULL,
      Nickname VARCHAR(50) NOT NULL,
      Email VARCHAR(50) NOT NULL,
      Status VARCHAR(50) NOT NULL,
      FOREIGN KEY (salespersonid) REFERENCES SalesPerson(salespersonid)
    );
    
    ALTER TABLE Users ADD CONSTRAINT username_lowercase CHECK (Username = LOWER(Username));
    ALTER TABLE Users ADD CONSTRAINT unique_person UNIQUE(salespersonid);
    ALTER TABLE Users ADD CONSTRAINT strong_password CHECK (Password ~ '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$');
    ALTER TABLE Users ADD CONSTRAINT valid_postion CHECK (Email ~ '^[a-z0-9._%+-]+@(gmail|hotmail|yahoo)\.com$');
    
    CREATE TABLE History_Change (
      ChangeID VARCHAR(5) PRIMARY KEY,
      Username VARCHAR(50),
      Selected_Table VARCHAR(50) NOT NULL,
      Location VARCHAR(50) NOT NULL,
      SubLocation VARCHAR(50) NOT NULL,
      Action VARCHAR(50) NOT NULL,
      Original_Data VARCHAR(50) NOT NULL,
      Updated_Data VARCHAR(50) NOT NULL,
      Date_Change DATE NOT NULL,
      Time_Change TIME NOT NULL,
      FOREIGN KEY (Username) REFERENCES Users(Username) ON UPDATE CASCADE ON DELETE SET NULL
    );
    
    ALTER TABLE History_Change ADD CONSTRAINT username_lowercase CHECK (Username = LOWER(Username));
    ALTER TABLE History_Change ADD CONSTRAINT table_lowercase CHECK (Selected_Table = LOWER(Selected_Table));
    ALTER TABLE History_Change ADD CONSTRAINT subloc_lowercase CHECK (SubLocation = LOWER(SubLocation));
    ALTER TABLE History_Change ADD CONSTRAINT valid_table_historychange CHECK (Selected_Table IN ('salesperson', 'sales', 'kpi', 'product', 'salesproduct', 'debtor', 'users', 'history_change'));
    ALTER TABLE History_Change ADD CONSTRAINT valid_action_historychange CHECK (Action IN ('Insert', 'Update', 'Delete', 'Restore', 'Banned', 'Unbanned', 'Login', 'Logout'));

# Indexing Attribute (Primary key always contain indexing)
    
    CREATE INDEX idx_gender ON SalesPerson(Gender);
    CREATE INDEX idx_position ON SalesPerson(Position);
    
    CREATE INDEX idx_spid_sales ON Sales(SalesPersonID);
    CREATE INDEX idx_year_sales ON Sales(Year);
    CREATE INDEX idx_month_sales ON Sales(Month);
    
    CREATE INDEX idx_product_status ON Product(Status);
    CREATE INDEX idx_importloc ON Product(ImportLoc);
    
    CREATE INDEX idx_status_salesproduct ON SalesProduct(Status);
    
    CREATE INDEX idx_company ON Debtor(CompanyName);
    CREATE INDEX idx_status_debor ON Debtor(Status);
    
    CREATE INDEX idx_users ON Users(Username);
    CREATE INDEX idx_password ON Users(Password);
    
    CREATE INDEX idx_username ON History_Change(Username);
    CREATE INDEX idx_selectedtable ON History_Change(Selected_Table);
    CREATE INDEX idx_action ON History_Change(Action);

# Insert Information
    Your code here...

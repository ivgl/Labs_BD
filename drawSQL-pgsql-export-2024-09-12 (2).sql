CREATE TABLE "products"(
    "ID" SERIAL NOT NULL,
    "Name" CHAR(255) NOT NULL
);
ALTER TABLE
    "products" ADD PRIMARY KEY("ID");
CREATE TABLE "price"(
    "ProductID" BIGINT NOT NULL,
    "Price" BIGINT NOT NULL
);
ALTER TABLE
    "price" ADD PRIMARY KEY("ProductID");
CREATE TABLE "return_possibility"(
    "ProductID" BIGINT NOT NULL,
    "ReturnPossibility" BOOLEAN NOT NULL
);
ALTER TABLE
    "return_possibility" ADD PRIMARY KEY("ProductID");
CREATE TABLE "storage_supplies"(
    "ProductID" BIGINT NOT NULL,
    "Amount" BIGINT NOT NULL
);
ALTER TABLE
    "storage_supplies" ADD PRIMARY KEY("ProductID");
CREATE TABLE "financials"(
    "ID" SERIAL NOT NULL,
    "Balance" BIGINT NOT NULL,
    "OrderID" BIGINT NULL
);
ALTER TABLE
    "financials" ADD PRIMARY KEY("ID");
CREATE TABLE "products_suppliers"(
    "ID" SERIAL NOT NULL,
    "SupplierID" BIGINT NOT NULL,
    "ProductID" BIGINT NOT NULL,
    "Price" DECIMAL(8, 2) NOT NULL,
    "DiscountMinAmount" BIGINT NOT NULL,
    "DiscountPercentage" DECIMAL(8, 2) NOT NULL
);
ALTER TABLE
    "products_suppliers" ADD PRIMARY KEY("ID");
CREATE TABLE "operation_types"(
    "ID" SERIAL NOT NULL,
    "Name" CHAR(255) NOT NULL
);
ALTER TABLE
    "operation_types" ADD PRIMARY KEY("ID");
CREATE TABLE "suppliers"(
    "ID" SERIAL NOT NULL,
    "Name" CHAR(255) NOT NULL
);
ALTER TABLE
    "suppliers" ADD PRIMARY KEY("ID");
CREATE TABLE "orders"(
    "ID" SERIAL NOT NULL,
    "TotalPrice" DECIMAL(8, 2) NOT NULL,
    "Dates" DATE NOT NULL,
    "OperationTypeID" BIGINT NOT NULL
);
ALTER TABLE
    "orders" ADD PRIMARY KEY("ID");
CREATE TABLE "orderItems"(
    "ID" SERIAL NOT NULL,
    "OrderID" BIGINT NOT NULL,
    "ProductID" BIGINT NOT NULL,
    "Amount" BIGINT NOT NULL
);
ALTER TABLE
    "orderItems" ADD PRIMARY KEY("ID");
ALTER TABLE
    "products_suppliers" ADD CONSTRAINT "products_suppliers_productid_foreign" FOREIGN KEY("ProductID") REFERENCES "products"("ID");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_operationtypeid_foreign" FOREIGN KEY("OperationTypeID") REFERENCES "operation_types"("ID");
ALTER TABLE
    "financials" ADD CONSTRAINT "financials_orderid_foreign" FOREIGN KEY("OrderID") REFERENCES "orders"("ID");
ALTER TABLE
    "storage_supplies" ADD CONSTRAINT "storage_supplies_productid_foreign" FOREIGN KEY("ProductID") REFERENCES "products"("ID");
ALTER TABLE
    "orderItems" ADD CONSTRAINT "orderitems_orderid_foreign" FOREIGN KEY("OrderID") REFERENCES "orders"("ID");
ALTER TABLE
    "price" ADD CONSTRAINT "price_productid_foreign" FOREIGN KEY("ProductID") REFERENCES "products"("ID");
ALTER TABLE
    "orderItems" ADD CONSTRAINT "orderitems_productid_foreign" FOREIGN KEY("ProductID") REFERENCES "products"("ID");
ALTER TABLE
    "return_possibility" ADD CONSTRAINT "return_possibility_productid_foreign" FOREIGN KEY("ProductID") REFERENCES "products"("ID");
ALTER TABLE
    "products_suppliers" ADD CONSTRAINT "products_suppliers_supplierid_foreign" FOREIGN KEY("SupplierID") REFERENCES "suppliers"("ID");
CREATE TABLE "products"(
    "ID" SERIAL NOT NULL,
    "Name" CHAR(255) NOT NULL,
    "ProductPrice" BIGINT NOT NULL,
    "ReturnPossibility" BOOLEAN NOT NULL,
    "StorageAmount" BIGINT NOT NULL
);
ALTER TABLE
    "products" ADD PRIMARY KEY("ID");
CREATE TABLE "financials"(
    "ID" SERIAL NOT NULL,
    "Balance" BIGINT NOT NULL
);
ALTER TABLE
    "financials" ADD PRIMARY KEY("ID");
CREATE TABLE "products_suppliers"(
    "ID" SERIAL NOT NULL,
    "SupplierID" BIGINT NOT NULL,
    "ProductID" BIGINT NOT NULL,
    "SupplierPrice" DECIMAL(8, 2) NOT NULL,
    "DiscountMinAmount" BIGINT NOT NULL,
    "DiscountPercentage" DECIMAL(8, 2) NOT NULL
);
ALTER TABLE
    "products_suppliers" ADD PRIMARY KEY("ID");
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
    "OperationType" CHAR(255) NOT NULL
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
    "orderItems" ADD CONSTRAINT "orderitems_orderid_foreign" FOREIGN KEY("OrderID") REFERENCES "orders"("ID");
ALTER TABLE
    "orderItems" ADD CONSTRAINT "orderitems_productid_foreign" FOREIGN KEY("ProductID") REFERENCES "products"("ID");
ALTER TABLE
    "products_suppliers" ADD CONSTRAINT "products_suppliers_supplierid_foreign" FOREIGN KEY("SupplierID") REFERENCES "suppliers"("ID");
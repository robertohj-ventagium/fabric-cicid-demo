CREATE TABLE [dbo].[Suppliers] (
    [SupplierKey]    INT            NOT NULL,
    [SupplierName]   VARCHAR (100)  NOT NULL,
    [SupplierRegion] VARCHAR (50)   NOT NULL,
    [SupplierType]   VARCHAR (50)   NOT NULL,
    [LeadTimeDays]   INT            NOT NULL,
    [ReliabilityPct] DECIMAL (5, 2) NOT NULL,
    [Active]         BIT            NOT NULL
);


GO


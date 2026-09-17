CREATE TABLE [dbo].[dim_product] (
    [ProductKey]      INT             NULL,
    [SKU]             NVARCHAR (MAX)  NULL,
    [ProductName]     NVARCHAR (MAX)  NULL,
    [Category]        NVARCHAR (MAX)  NULL,
    [CategoryCode]    NVARCHAR (MAX)  NULL,
    [Subcategory]     NVARCHAR (MAX)  NULL,
    [SubcategoryCode] NVARCHAR (MAX)  NULL,
    [Brand]           NVARCHAR (MAX)  NULL,
    [UnitListPrice]   DECIMAL (10, 2) NULL,
    [UnitCost]        DECIMAL (10, 2) NULL,
    [PackSize]        NVARCHAR (MAX)  NULL,
    [UnitOfMeasure]   NVARCHAR (MAX)  NULL,
    [LaunchDate]      DATE            NULL,
    [IsSeasonal]      INT             NULL,
    [LifecycleStatus] NVARCHAR (MAX)  NULL
);


GO


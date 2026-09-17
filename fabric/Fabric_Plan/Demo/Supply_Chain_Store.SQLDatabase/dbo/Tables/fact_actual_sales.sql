CREATE TABLE [dbo].[fact_actual_sales] (
    [DateKey]          INT             NULL,
    [StoreKey]         INT             NULL,
    [ProductKey]       INT             NULL,
    [ActualQuantity]   DECIMAL (12, 2) NULL,
    [GrossRevenue]     DECIMAL (14, 2) NULL,
    [DiscountAmount]   DECIMAL (14, 2) NULL,
    [NetRevenue]       DECIMAL (15, 2) NULL,
    [TransactionCount] INT             NULL,
    [PromotionFlag]    INT             NULL,
    [PromotionID]      NVARCHAR (MAX)  NULL,
    [LoadedAt]         DATETIME2 (7)   NULL
);


GO


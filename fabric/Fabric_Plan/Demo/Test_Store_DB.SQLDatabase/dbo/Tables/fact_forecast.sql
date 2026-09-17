CREATE TABLE [dbo].[fact_forecast] (
    [ForecastID]        BIGINT          NULL,
    [ForecastVersion]   NVARCHAR (MAX)  NULL,
    [ForecastVersionID] INT             NULL,
    [CreationDateKey]   INT             NULL,
    [ForecastDateKey]   INT             NULL,
    [StoreKey]          INT             NULL,
    [ProductKey]        INT             NULL,
    [ForecastQuantity]  DECIMAL (12, 2) NULL,
    [ForecastRevenue]   DECIMAL (14, 2) NULL,
    [LowerBound]        DECIMAL (12, 2) NULL,
    [UpperBound]        DECIMAL (12, 2) NULL,
    [ForecastModel]     NVARCHAR (MAX)  NULL,
    [CreatedBy]         NVARCHAR (MAX)  NULL,
    [CreatedAt]         DATETIME2 (7)   NULL
);


GO


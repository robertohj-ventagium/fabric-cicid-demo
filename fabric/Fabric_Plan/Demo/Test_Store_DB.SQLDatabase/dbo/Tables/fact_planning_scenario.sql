CREATE TABLE [dbo].[fact_planning_scenario] (
    [ScenarioID]            BIGINT          NULL,
    [ScenarioName]          NVARCHAR (MAX)  NULL,
    [ScenarioDescription]   NVARCHAR (MAX)  NULL,
    [BaseForecastVersionID] INT             NULL,
    [DateKey]               INT             NULL,
    [StoreKey]              INT             NULL,
    [ProductKey]            INT             NULL,
    [AdjustmentType]        NVARCHAR (MAX)  NULL,
    [AdjustmentPct]         DECIMAL (7, 4)  NULL,
    [AdjustmentAbsolute]    DECIMAL (12, 2) NULL,
    [BaselineForecast]      DECIMAL (12, 2) NULL,
    [AdjustedForecast]      DECIMAL (12, 2) NULL,
    [CreatedBy]             NVARCHAR (MAX)  NULL,
    [CreatedAt]             DATETIME2 (7)   NULL,
    [IsActive]              INT             NULL
);


GO


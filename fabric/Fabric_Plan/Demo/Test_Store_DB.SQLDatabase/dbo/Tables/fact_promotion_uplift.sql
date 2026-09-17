CREATE TABLE [dbo].[fact_promotion_uplift] (
    [UpliftKey]    INT            NULL,
    [Category]     NVARCHAR (MAX) NULL,
    [Subcategory]  NVARCHAR (MAX) NULL,
    [WeekNumber]   INT            NULL,
    [UpliftPct]    FLOAT (53)     NULL,
    [ScenarioName] NVARCHAR (MAX) NULL,
    [CreatedBy]    NVARCHAR (MAX) NULL,
    [CreatedAt]    DATETIME2 (7)  NULL
);


GO


CREATE TABLE [dbo].[FactFinance] (
    [FinanceKey]         INT        NOT NULL,
    [DateKey]            INT        NOT NULL,
    [OrganizationKey]    INT        NOT NULL,
    [DepartmentGroupKey] INT        NOT NULL,
    [ScenarioKey]        INT        NOT NULL,
    [AccountKey]         INT        NOT NULL,
    [Amount]             FLOAT (53) NOT NULL,
    [AmountCorrected]    FLOAT (53) NULL
);


GO


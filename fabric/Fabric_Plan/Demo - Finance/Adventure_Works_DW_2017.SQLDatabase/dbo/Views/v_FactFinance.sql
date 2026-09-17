CREATE VIEW v_FactFinance AS
SELECT [FinanceKey]
      ,[DateKey]
      ,[OrganizationKey]
      ,[DepartmentGroupKey]
      ,[ScenarioKey]
      ,[AccountKey]
      ,[Amount]
  FROM [dbo].[FactFinance]

GO


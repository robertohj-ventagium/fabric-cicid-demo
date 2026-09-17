CREATE TABLE [dbo].[DimAccountHierarchy] (
    [AccountKey]                    INT             NOT NULL,
    [ParentAccountKey]              INT             NULL,
    [AccountCodeAlternateKey]       NVARCHAR (50)   NULL,
    [ParentAccountCodeAlternateKey] NVARCHAR (50)   NULL,
    [AccountDescription]            NVARCHAR (50)   NULL,
    [AccountType]                   NVARCHAR (50)   NULL,
    [Operator]                      NVARCHAR (50)   NULL,
    [CustomMembers]                 NVARCHAR (200)  NULL,
    [ValueType]                     NVARCHAR (50)   NULL,
    [CustomMemberOptions]           NVARCHAR (255)  NULL,
    [HierarchyLevel]                INT             NOT NULL,
    [Level1]                        NVARCHAR (200)  NULL,
    [Level2]                        NVARCHAR (200)  NULL,
    [Level3]                        NVARCHAR (200)  NULL,
    [Level4]                        NVARCHAR (200)  NULL,
    [Level5]                        NVARCHAR (200)  NULL,
    [Level6]                        NVARCHAR (200)  NULL,
    [Level7]                        NVARCHAR (200)  NULL,
    [Level8]                        NVARCHAR (200)  NULL,
    [Level9]                        NVARCHAR (200)  NULL,
    [Level10]                       NVARCHAR (200)  NULL,
    [Budget]                        DECIMAL (10, 2) NULL
);


GO


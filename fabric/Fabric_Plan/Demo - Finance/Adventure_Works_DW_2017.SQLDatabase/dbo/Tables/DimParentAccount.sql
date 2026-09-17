CREATE TABLE [dbo].[DimParentAccount] (
    [AccountKey]                    INT            NOT NULL,
    [ParentAccountKey]              INT            NULL,
    [AccountCodeAlternateKey]       INT            NULL,
    [ParentAccountCodeAlternateKey] INT            NULL,
    [AccountDescription]            NVARCHAR (50)  NULL,
    [AccountType]                   NVARCHAR (50)  NULL,
    [Operator]                      NVARCHAR (50)  NULL,
    [CustomMembers]                 NVARCHAR (300) NULL,
    [ValueType]                     NVARCHAR (50)  NULL,
    [CustomMemberOptions]           NVARCHAR (200) NULL
);


GO


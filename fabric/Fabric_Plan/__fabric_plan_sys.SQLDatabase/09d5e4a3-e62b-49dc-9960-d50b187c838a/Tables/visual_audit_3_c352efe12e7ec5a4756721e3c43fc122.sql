CREATE TABLE [09d5e4a3-e62b-49dc-9960-d50b187c838a].[visual_audit_3_c352efe12e7ec5a4756721e3c43fc122] (
    [id]                         BIGINT          IDENTITY (1, 1) NOT NULL,
    [rowId]                      NVARCHAR (2048) NOT NULL,
    [colId]                      NVARCHAR (2048) NOT NULL,
    [scenarioGuid]               NVARCHAR (255)  NULL,
    [measureGuid]                NVARCHAR (255)  NULL,
    [filterContextHash]          NVARCHAR (255)  NULL,
    [action]                     NVARCHAR (255)  NULL,
    [meta]                       NVARCHAR (MAX)  NULL,
    [oldValue]                   NVARCHAR (MAX)  NULL,
    [newValue]                   NVARCHAR (MAX)  NULL,
    [updatedAt]                  INT             NOT NULL,
    [updatedByUPN]               NVARCHAR (320)  NOT NULL,
    [updatedBy]                  NVARCHAR (128)  NOT NULL,
    [dim_dim_productCategory]    NVARCHAR (255)  NULL,
    [dim_dim_productSubcategory] NVARCHAR (255)  NULL,
    [dim_dim_productSKU]         NVARCHAR (255)  NULL,
    [dim_dim_dateMonthYear]      NVARCHAR (255)  NULL,
    PRIMARY KEY CLUSTERED ([id] ASC)
);


GO


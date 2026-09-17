CREATE TABLE [ff0a9f2b-a2de-423e-aec7-20903c1daf57].[visual_audit_1_24426588dff29e993d038c62aeedb547] (
    [id]                                     BIGINT          IDENTITY (1, 1) NOT NULL,
    [rowId]                                  NVARCHAR (2048) NOT NULL,
    [colId]                                  NVARCHAR (2048) NOT NULL,
    [scenarioGuid]                           NVARCHAR (255)  NULL,
    [measureGuid]                            NVARCHAR (255)  NULL,
    [filterContextHash]                      NVARCHAR (255)  NULL,
    [action]                                 NVARCHAR (255)  NULL,
    [meta]                                   NVARCHAR (MAX)  NULL,
    [oldValue]                               NVARCHAR (MAX)  NULL,
    [newValue]                               NVARCHAR (MAX)  NULL,
    [updatedAt]                              INT             NOT NULL,
    [updatedByUPN]                           NVARCHAR (320)  NOT NULL,
    [updatedBy]                              NVARCHAR (128)  NOT NULL,
    [dim_DimParentAccountAccountDescription] NVARCHAR (255)  NULL,
    [dim_DimAccountAccountDescription]       NVARCHAR (255)  NULL,
    [dim_DimDateCalendarYear]                NVARCHAR (255)  NULL,
    [dim_DimDateCalendarQuarter]             NVARCHAR (255)  NULL,
    [dim_DimScenarioScenarioName]            NVARCHAR (255)  NULL,
    PRIMARY KEY CLUSTERED ([id] ASC)
);


GO


CREATE TABLE [ff0a9f2b-a2de-423e-aec7-20903c1daf57].[visual_di_1_ee5953ed89ee56d0a233c4337ace8de4] (
    [id]                                     BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                                  NVARCHAR (255)   NOT NULL,
    [colId]                                  NVARCHAR (255)   NOT NULL,
    [scenarioId]                             INT              NULL,
    [filterContextHash]                      NVARCHAR (255)   NULL,
    [updatedAt]                              INT              NOT NULL,
    [updatedBy]                              NVARCHAR (128)   NOT NULL,
    [dim_DimParentAccountAccountDescription] NVARCHAR (255)   NULL,
    [dim_DimAccountAccountDescription]       NVARCHAR (255)   NULL,
    [dim_DimDateCalendarYear]                NVARCHAR (255)   NULL,
    [dim_DimDateCalendarQuarter]             NVARCHAR (255)   NULL,
    [dim_DimDateEnglishMonthName]            NVARCHAR (255)   NULL,
    [dim_DimScenarioScenarioName]            NVARCHAR (255)   NULL,
    [measure_1]                              DECIMAL (30, 10) NULL,
    [measure_7]                              DECIMAL (30, 10) NULL,
    [measure_1_meta]                         NVARCHAR (255)   NULL,
    [measure_7_meta]                         NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


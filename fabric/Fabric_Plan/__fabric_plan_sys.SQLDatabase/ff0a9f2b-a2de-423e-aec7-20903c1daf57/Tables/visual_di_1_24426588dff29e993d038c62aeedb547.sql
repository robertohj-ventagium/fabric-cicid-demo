CREATE TABLE [ff0a9f2b-a2de-423e-aec7-20903c1daf57].[visual_di_1_24426588dff29e993d038c62aeedb547] (
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
    [dim_DimScenarioScenarioName]            NVARCHAR (255)   NULL,
    [measure_1]                              DECIMAL (30, 10) NULL,
    [measure_1_meta]                         NVARCHAR (255)   NULL,
    [measure_7]                              DECIMAL (30, 10) NULL,
    [measure_7_meta]                         NVARCHAR (255)   NULL,
    [measure_12]                             DECIMAL (30, 10) NULL,
    [measure_12_meta]                        NVARCHAR (255)   NULL,
    [measure_13]                             NVARCHAR (MAX)   NULL,
    [measure_13_meta]                        NVARCHAR (255)   NULL,
    [measure_14]                             NVARCHAR (255)   NULL,
    [measure_14_meta]                        NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


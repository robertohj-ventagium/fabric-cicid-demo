CREATE TABLE [ff0a9f2b-a2de-423e-aec7-20903c1daf57].[visual_di_1_f0c7abb3b3ed8fec70eee87555aa1a66] (
    [id]                                                    BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                                                 NVARCHAR (255)   NOT NULL,
    [colId]                                                 NVARCHAR (255)   NOT NULL,
    [scenarioId]                                            INT              NULL,
    [filterContextHash]                                     NVARCHAR (255)   NULL,
    [updatedAt]                                             INT              NOT NULL,
    [updatedBy]                                             NVARCHAR (128)   NOT NULL,
    [dim_DimParentAccountAccountDescription]                NVARCHAR (255)   NULL,
    [dim_DimAccountAccountDescription]                      NVARCHAR (255)   NULL,
    [dim_DimDateCalendarYearJerarquaDimDateCalendarYear]    NVARCHAR (255)   NULL,
    [dim_DimDateCalendarYearJerarquaDimDateCalendarQuarter] NVARCHAR (255)   NULL,
    [dim_DimScenarioScenarioName]                           NVARCHAR (255)   NULL,
    [measure_1]                                             DECIMAL (30, 10) NULL,
    [measure_1_meta]                                        NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


CREATE TABLE [09d5e4a3-e62b-49dc-9960-d50b187c838a].[visual_di_3_71d1e2720ba03ffde3e25609803ec720] (
    [id]                                            BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                                         NVARCHAR (255)   NOT NULL,
    [colId]                                         NVARCHAR (255)   NOT NULL,
    [scenarioId]                                    INT              NULL,
    [filterContextHash]                             NVARCHAR (255)   NULL,
    [updatedAt]                                     INT              NOT NULL,
    [updatedBy]                                     NVARCHAR (128)   NOT NULL,
    [dim_fact_planning_scenarioAdjustmentType]      NVARCHAR (255)   NULL,
    [dim_fact_planning_scenarioCreatedBy]           NVARCHAR (255)   NULL,
    [dim_fact_planning_scenarioIsActive]            NVARCHAR (255)   NULL,
    [dim_fact_planning_scenarioScenarioDescription] NVARCHAR (255)   NULL,
    [dim_fact_planning_scenarioScenarioName]        NVARCHAR (255)   NULL,
    [measure_9]                                     DECIMAL (30, 10) NULL,
    [measure_9_meta]                                NVARCHAR (255)   NULL,
    [measure_10]                                    DECIMAL (30, 10) NULL,
    [measure_10_meta]                               NVARCHAR (255)   NULL,
    [measure_11]                                    DECIMAL (30, 10) NULL,
    [measure_11_meta]                               NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


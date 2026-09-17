CREATE TABLE [af90de62-bacf-48d1-81f6-23d388f100e3].[visual_di_1_3ac191b1b04b0bcd85053d9138a150d9] (
    [id]                         BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                      NVARCHAR (255)   NOT NULL,
    [colId]                      NVARCHAR (255)   NOT NULL,
    [scenarioId]                 INT              NULL,
    [filterContextHash]          NVARCHAR (255)   NULL,
    [updatedAt]                  INT              NOT NULL,
    [updatedBy]                  NVARCHAR (128)   NOT NULL,
    [dim_dim_storeStoreName]     NVARCHAR (255)   NULL,
    [dim_dim_productCategory]    NVARCHAR (255)   NULL,
    [dim_dim_productProductName] NVARCHAR (255)   NULL,
    [dim_dim_dateWeekStartDate]  NVARCHAR (255)   NULL,
    [measure_3]                  DECIMAL (30, 10) NULL,
    [measure_5]                  DECIMAL (30, 10) NULL,
    [measure_6]                  DECIMAL (30, 10) NULL,
    [measure_3_meta]             NVARCHAR (255)   NULL,
    [measure_5_meta]             NVARCHAR (255)   NULL,
    [measure_6_meta]             NVARCHAR (255)   NULL,
    [measure_8]                  DECIMAL (30, 10) NULL,
    [measure_8_meta]             NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO


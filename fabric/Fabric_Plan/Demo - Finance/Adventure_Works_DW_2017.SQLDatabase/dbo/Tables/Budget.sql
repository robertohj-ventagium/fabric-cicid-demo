CREATE TABLE [dbo].[Budget] (
    [IrId]                 INT             IDENTITY (1, 1) NOT NULL,
    [IrScenario]           NVARCHAR (512)  NULL,
    [Level1]               NVARCHAR (512)  NULL,
    [Level2]               NVARCHAR (512)  NULL,
    [Level3]               NVARCHAR (512)  NULL,
    [Level4]               NVARCHAR (512)  NULL,
    [Level5]               NVARCHAR (512)  NULL,
    [Level6]               NVARCHAR (512)  NULL,
    [Calendaryear]         NVARCHAR (512)  NULL,
    [Calendarquarter]      NVARCHAR (512)  NULL,
    [Scenarioname]         NVARCHAR (512)  NULL,
    [ValueColumnName]      NVARCHAR (512)  NULL,
    [Value]                NUMERIC (25, 2) NULL,
    [ValueText]            NVARCHAR (MAX)  NULL,
    [LastUpdatedAt]        DATETIME2 (7)   NULL,
    [LastUpdatedBy]        NVARCHAR (512)  NULL,
    [Source]               NVARCHAR (512)  NULL,
    [IrNotes]              NVARCHAR (MAX)  NULL,
    [IrComments]           NVARCHAR (MAX)  NULL,
    [IrCellMeta]           NVARCHAR (MAX)  NULL,
    [IrWritebackUser]      NVARCHAR (512)  NULL,
    [IrWritebackTimestamp] DATETIME2 (7)   NULL,
    PRIMARY KEY CLUSTERED ([IrId] ASC)
);


GO


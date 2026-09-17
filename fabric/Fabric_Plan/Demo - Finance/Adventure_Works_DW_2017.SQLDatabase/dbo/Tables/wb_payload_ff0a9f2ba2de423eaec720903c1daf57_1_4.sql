CREATE TABLE [dbo].[wb_payload_ff0a9f2ba2de423eaec720903c1daf57_1_4] (
    [Level1]            NVARCHAR (512) NULL,
    [Level2]            NVARCHAR (512) NULL,
    [Level3]            NVARCHAR (512) NULL,
    [Level4]            NVARCHAR (512) NULL,
    [Level5]            NVARCHAR (512) NULL,
    [Level6]            NVARCHAR (512) NULL,
    [Accountkey]        NVARCHAR (512) NULL,
    [Calendaryear]      NVARCHAR (512) NULL,
    [Calendarquarter]   NVARCHAR (512) NULL,
    [Datekey]           NVARCHAR (512) NULL,
    [ValueColumnName]   NVARCHAR (512) NULL,
    [Value]             NVARCHAR (MAX) NULL,
    [Source]            NVARCHAR (512) NULL,
    [IrNotes]           NVARCHAR (MAX) NULL,
    [IrScenario]        NVARCHAR (512) NULL,
    [CellId]            NVARCHAR (512) NULL,
    [IsAggregated]      TINYINT        CONSTRAINT [wb_payload_ff0a9f2ba2de423eaec720903c1daf57_1_4_isaggregated_default] DEFAULT ('1') NULL,
    [FilterContextHash] NVARCHAR (512) NULL,
    [ExecutionId]       NVARCHAR (512) NULL,
    [IrId]              NVARCHAR (512) NULL
);


GO


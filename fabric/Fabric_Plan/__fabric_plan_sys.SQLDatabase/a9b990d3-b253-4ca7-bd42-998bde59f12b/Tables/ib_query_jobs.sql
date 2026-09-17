CREATE TABLE [a9b990d3-b253-4ca7-bd42-998bde59f12b].[ib_query_jobs] (
    [id]            INT            IDENTITY (1, 1) NOT NULL,
    [jobId]         VARCHAR (255)  NOT NULL,
    [queryId]       INT            NULL,
    [scheduledTime] INT            NOT NULL,
    [startTime]     INT            NULL,
    [endTime]       INT            NULL,
    [errorCode]     NVARCHAR (MAX) NULL,
    [jobType]       INT            NOT NULL,
    [jobMeta]       NVARCHAR (MAX) NULL,
    [visualId]      INT            NULL,
    [sourceId]      INT            NULL,
    [status]        INT            CONSTRAINT [DF_58b1d55430602f14b0157764ecf] DEFAULT ((10)) NOT NULL,
    [createdBy]     NVARCHAR (128) NOT NULL,
    [updatedBy]     NVARCHAR (128) NOT NULL,
    [createdAt]     INT            NOT NULL,
    [updatedAt]     INT            NOT NULL,
    CONSTRAINT [PK_9042d449d37ea29e79b839004b5] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT [FK_19ca13da60070ea18bb5e1784ce] FOREIGN KEY ([visualId]) REFERENCES [a9b990d3-b253-4ca7-bd42-998bde59f12b].[visual] ([id]),
    CONSTRAINT [FK_9beab4544f96bf0b29fb14b8ab5] FOREIGN KEY ([sourceId]) REFERENCES [a9b990d3-b253-4ca7-bd42-998bde59f12b].[ib_source] ([id]),
    CONSTRAINT [FK_d740d71a6feeedf50cfe957047d] FOREIGN KEY ([queryId]) REFERENCES [a9b990d3-b253-4ca7-bd42-998bde59f12b].[ib_queries] ([id]) ON DELETE CASCADE
);


GO

CREATE NONCLUSTERED INDEX [idx_ib_query_jobs_createdAt]
    ON [a9b990d3-b253-4ca7-bd42-998bde59f12b].[ib_query_jobs]([createdAt] ASC);


GO

CREATE NONCLUSTERED INDEX [idx_ib_query_jobs_jobId]
    ON [a9b990d3-b253-4ca7-bd42-998bde59f12b].[ib_query_jobs]([jobId] ASC);


GO

CREATE NONCLUSTERED INDEX [idx_ib_query_jobs_jobType_queryId]
    ON [a9b990d3-b253-4ca7-bd42-998bde59f12b].[ib_query_jobs]([jobType] ASC, [queryId] ASC);


GO

CREATE NONCLUSTERED INDEX [idx_ib_query_jobs_queryId_visualId_sourceId]
    ON [a9b990d3-b253-4ca7-bd42-998bde59f12b].[ib_query_jobs]([queryId] ASC, [visualId] ASC, [sourceId] ASC);


GO

CREATE NONCLUSTERED INDEX [idx_ib_query_jobs_status_startTime]
    ON [a9b990d3-b253-4ca7-bd42-998bde59f12b].[ib_query_jobs]([status] ASC, [startTime] ASC);


GO


CREATE TABLE [f1f15b4e-9b3e-482c-a6a4-b5f905b7f6e0].[powertable_visual_source] (
    [id]        INT            IDENTITY (1, 1) NOT NULL,
    [visualId]  INT            NOT NULL,
    [sourceId]  INT            NOT NULL,
    [status]    INT            CONSTRAINT [DF_af2b9acbbac7d2021445bfc43d6] DEFAULT ((10)) NOT NULL,
    [createdBy] NVARCHAR (128) NOT NULL,
    [updatedBy] NVARCHAR (128) NOT NULL,
    [createdAt] INT            NOT NULL,
    [updatedAt] INT            NOT NULL,
    CONSTRAINT [PK_0c26bad688242783eff7c5d4912] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT [FK_2d2674056f7c38b4b62b2b3c7e4] FOREIGN KEY ([sourceId]) REFERENCES [f1f15b4e-9b3e-482c-a6a4-b5f905b7f6e0].[powertable_source] ([id]),
    CONSTRAINT [FK_40aea1c78e8c4b9ded7a7e28ee5] FOREIGN KEY ([visualId]) REFERENCES [f1f15b4e-9b3e-482c-a6a4-b5f905b7f6e0].[visual] ([id])
);


GO


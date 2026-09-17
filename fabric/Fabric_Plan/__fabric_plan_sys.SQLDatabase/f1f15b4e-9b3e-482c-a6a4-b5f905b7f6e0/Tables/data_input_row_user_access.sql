CREATE TABLE [f1f15b4e-9b3e-482c-a6a4-b5f905b7f6e0].[data_input_row_user_access] (
    [id]               INT            IDENTITY (1, 1) NOT NULL,
    [visualId]         INT            NOT NULL,
    [accessEntityType] INT            NOT NULL,
    [accessEntityId]   VARCHAR (128)  NOT NULL,
    [status]           INT            CONSTRAINT [DF_6ed52463604d2b4a73fd013b134] DEFAULT ((10)) NOT NULL,
    [createdBy]        NVARCHAR (128) NOT NULL,
    [updatedBy]        NVARCHAR (128) NOT NULL,
    [createdAt]        INT            NOT NULL,
    [updatedAt]        INT            NOT NULL,
    CONSTRAINT [PK_e22d4f23b6ecb3e536ed885a2ce] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT [FK_4278b147378e9929cdc885a191b] FOREIGN KEY ([visualId]) REFERENCES [f1f15b4e-9b3e-482c-a6a4-b5f905b7f6e0].[visual] ([id])
);


GO


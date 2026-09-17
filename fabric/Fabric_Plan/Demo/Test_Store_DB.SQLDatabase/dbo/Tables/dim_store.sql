CREATE TABLE [dbo].[dim_store] (
    [StoreKey]     INT            NULL,
    [StoreID]      NVARCHAR (MAX) NULL,
    [StoreName]    NVARCHAR (MAX) NULL,
    [Region]       NVARCHAR (MAX) NULL,
    [Market]       NVARCHAR (MAX) NULL,
    [Country]      NVARCHAR (MAX) NULL,
    [State]        NVARCHAR (MAX) NULL,
    [City]         NVARCHAR (MAX) NULL,
    [StoreFormat]  NVARCHAR (MAX) NULL,
    [StoreSizeSqM] INT            NULL,
    [OpenDate]     DATE           NULL,
    [StoreStatus]  NVARCHAR (MAX) NULL
);


GO


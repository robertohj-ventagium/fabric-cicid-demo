CREATE TABLE [dbo].[dim_date] (
    [DateKey]        INT            NULL,
    [Date]           DATE           NULL,
    [DayOfWeek]      INT            NULL,
    [DayName]        NVARCHAR (MAX) NULL,
    [WeekNumber]     INT            NULL,
    [WeekStartDate]  DATE           NULL,
    [MonthNumber]    INT            NULL,
    [MonthName]      NVARCHAR (MAX) NULL,
    [MonthYear]      NVARCHAR (MAX) NULL,
    [Quarter]        INT            NULL,
    [Year]           INT            NULL,
    [FiscalPeriod]   INT            NULL,
    [FiscalQuarter]  INT            NULL,
    [FiscalYear]     INT            NULL,
    [IsWeekend]      INT            NULL,
    [IsHoliday]      INT            NULL,
    [HolidayName]    NVARCHAR (MAX) NULL,
    [RetailSeason]   NVARCHAR (MAX) NULL,
    [WeeksFromToday] INT            NULL
);


GO


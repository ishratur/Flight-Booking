USE [mirahman354]
GO
/****** Object:  Trigger [dbo].[tr_seatAvailability]    Script Date: 04/11/2018 23:08:57 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER TRIGGER [dbo].[tr_seatAvailability] ON [dbo].[Booking] AFTER INSERT, DELETE
AS
BEGIN
UPDATE Flight_Instance
SET available_seats = available_seats - (SELECT COUNT(*)
FROM inserted
WHERE 
Flight_Instance.flight_code = inserted.flight_code AND 
Flight_Instance.depart_date = inserted.depart_date)


UPDATE Flight_Instance
SET available_seats = available_seats + (SELECT COUNT(*)
FROM deleted
WHERE 
Flight_Instance.flight_code = deleted.flight_code AND 
Flight_Instance.depart_date = deleted.depart_date)
	
END
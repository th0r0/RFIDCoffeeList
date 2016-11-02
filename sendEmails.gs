// Send email with coffee invoice
function sendEmails() {
  
  // Get and format current date, we only need it for the email subject
  var date = new Date();
  var dateOfDay = new Date(date.getTime());
  var dateFormatted = Utilities.formatDate(dateOfDay, "Europe/Berlin", "yyyy-MM");
    
  // Get reference to sheet with coffee list
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Users");

  if (sheet == null) {
    Logger.log("Sheet not found");
    return;
  }
  
  // First row with data to process
  var startRow = 2;  
  
  // Get last row with filled data
  var lastRow = sheet.getLastRow() - 1;
  
  Logger.log("lastRow: " + lastRow);
  
  
  // Fetch the range of cells that contain data
  var dataRange = sheet.getRange(startRow, 1, lastRow, 5)
  
  // Fetch values for each row in the Range.
  var data = dataRange.getValues();
  
  for (i in data) {
    var row = data[i];
    var id = row[0];  
    var coffeeAmount = row[1];
    var name = row[2];
    var emailAddress = row[3];
    var cost = row[4];
    
    // URL to picture to use as inline HTML element
    var coffeeLogoUrl = "https://openclipart.org/image/300px/svg_to_png/264683/I-heart-Coffee.png&disposition=attachment";
    
    // Fetch picture and store it as blob
    var coffeeLogoBlob = UrlFetchApp.fetch(coffeeLogoUrl).getBlob().setName("coffeeLogoBlob");
    
    // Send email
    MailApp.sendEmail({
      to: emailAddress,
      subject: "Kaffeerechnung " + dateFormatted,
      
      // TODO: Change size of 
      htmlBody: "<img src='cid:coffeeLogo' style='width:142px; height:79px;'><br>" +
              "Sie haben " + coffeeAmount  + " Kaffee für " + cost  + " € getrunken.",
      inlineImages:
       {
         coffeeLogo: coffeeLogoBlob
       }
   });

    
    
    
    
    // Build subject
    //var subject = "Kaffeerechnung " + dateFormatted;
    
    // Build email body
    //message = "Sie haben " + coffeeAmount  + " Kaffee für " + cost  + " € getrunken.";
    
    // Send email
    //MailApp.sendEmail(emailAddress, subject, message);
  }

  
  
}

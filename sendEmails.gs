// Send email with coffee invoice
function sendEmails() {
  
  // Get and format current date, we only need it for the email subject
  var date = new Date();
  var dateOfDay = new Date(date.getTime());
  var dateFormatted = Utilities.formatDate(dateOfDay, "Europe/Berlin", "yyyy-MM");
  
  // URL to picture to use as inline HTML element
  var coffeeLogoUrl = "https://openclipart.org/image/300px/svg_to_png/104185/1294538687.png&disposition=attachment";
    
  // Fetch picture and store it as blob
  var coffeeLogoBlob = UrlFetchApp.fetch(coffeeLogoUrl).getBlob().setName("coffeeLogoBlob");
  
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
    
    // Valid email address found
    if (emailAddress != ""){
    
      // Send email
      MailApp.sendEmail({
                          to: emailAddress,
                          subject: "Kaffeerechnung " + dateFormatted,
                          htmlBody: "<img src='cid:coffeeLogo' style='width:50px; height:52px;'><br>" +
                                   "Hallo " + name + ",<br>" +
                                   "Die Kaffeerechnung ist mal wieder fällig.<br>" +
                                   "Sie haben <b>" + coffeeAmount  + " Kaffee</b> für <b>" + cost  + " €</b> getrunken.<br>" +
                                   "Bitte den Betrag per PayPal an 'thorge.andersen@man.eu' senden,<br>" +
                                   "oder einfach den PayPalMe-Link verwenden http://paypal.me/coffeeMDT/" + cost + "<br>" +
                                   "Mehr info hier: https://www.paypal.com/de/webapps/mpp/send-money-online<br>" +
                                   "und hier: https://www.paypal.me<br>" +
                                   "Wichtig: Senden an Freunde und Familie auswählen, sonst gönnt sich PayPal eine Transaktionsgebühr ;)<br>" + 
                                   "Gruß<br>"+
                                   "Dein RasPi",
                         inlineImages:{
                                        coffeeLogo: coffeeLogoBlob
                         }
      });
    } // Valid email found

  }

  
}

var fs = require('fs');
var plist = require('plist');
var jsonObj = JSON.parse(fs.readFileSync('PlantUML-tmLanguage.json', 'utf8'));

fs.writeFile('PlantUML.tmLanguage', plist.build(jsonObj));
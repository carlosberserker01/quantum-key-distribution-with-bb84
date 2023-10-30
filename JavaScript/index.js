let table
let tableBody
let isEva = false
let arrayFinal = []

const createTableRow = () => {
  isEva = document.querySelector('#checkbox-eva').checked

  //Alice processes...
  let tableRowArray = []

  //Create Bit Alice
  let randomAliceBit = Math.round(Math.random())
  tableRowArray.push(randomAliceBit)

  //Create Base Alice
  let randomAliceBase = Math.round(Math.random())
  tableRowArray.push(randomAliceBase)

  //Create Qubit Alice
  tableRowArray.push(calculateAliceQubit(randomAliceBit, randomAliceBase))

  //Eva processes...
  if (isEva) {
    //Create Base Eva
    let randomEvaBase = Math.round(Math.random())
    tableRowArray.push(randomEvaBase)

    //Create Qubit Eva
    tableRowArray.push(calculateQubit(tableRowArray[2], randomEvaBase))
  } 

  //Bob processes...
  //Create Base Bob
  let randomBobBase = Math.round(Math.random())
  tableRowArray.push(randomBobBase)

  //If Eva is present calculate Qubit between Qubit Eva and BaseBob
  if (isEva) {
    tableRowArray.push(calculateQubit(tableRowArray[4], randomBobBase))
  } else { // else if Eva isn't present, calculate Qubit between Qubit Alice and Base Bob
    tableRowArray.push(calculateQubit(tableRowArray[2], randomBobBase))
  }

  //Alternative code
  // tableRowArray.push(calculateQubit(tableRowArray[isEva ? 4 : 2], randomBobBase))

  // Render elements for each row
  let row = document.createElement("tr")
  for (let i = 0; i < tableRowArray.length; i++) {
    let td = document.createElement("td")
    let tdText = document.createTextNode(`${tableRowArray[i]}`)
    td.appendChild(tdText)
    row.appendChild(td)
  }

  //Agrega el row al tablebody
  tableBody.appendChild(row)
  //Agrega el tablebody a la tabla
  table.appendChild(tableBody)

  //Selecciona el tablesContainer
  let tablesContainer = document.querySelector('.tables-container')

  //Crea un div llamado divTable
  let divTable = document.createElement("div")

  //Agrega el divtable
  tablesContainer.appendChild(divTable)
  let mainContainer = document.querySelector('.main-container')
  mainContainer.appendChild(table)

  if (isEva) {
    if (tableRowArray[1] === tableRowArray[5]) {
      if (!(tableRowArray[2] === tableRowArray[6])){
        arrayFinal.push(1)
      } 
    }
  } else {
    if (tableRowArray[1] === tableRowArray[3]){
      arrayFinal.push(tableRowArray[0])
    }
  }
}

// Calculate between 0-0, 0-1, 1-0, 1-1
const calculateAliceQubit = (randomBobBit, randomBobBase) => {
  if (randomBobBit === 0 && randomBobBase === 0) {
    return "|0>"
  }
  if (randomBobBit === 0 && randomBobBase === 1) {
    return "|+>"
  }
  if (randomBobBit === 1 && randomBobBase === 0) {
    return "|1>"
  }
  if (randomBobBit === 1 && randomBobBase === 1) {
    return "|->"
  }
}

const calculateQubit = (receivedQubit, randomBobBase) => {
  if (receivedQubit === "|0>" && randomBobBase === 0) {
    return "|0>"
  }
  if (receivedQubit === "|0>" && randomBobBase === 1) {
    let tmp = Math.round(Math.random())
    return tmp === 0 ? "|+>" : "|->"
  }
  if (receivedQubit === "|1>" && randomBobBase === 0) {
    return "|1>"
  }
  if (receivedQubit === "|1>" && randomBobBase === 1) {
    let tmp = Math.round(Math.random())
    return tmp === 0 ? "|+>" : "|->"
  }


  if (receivedQubit === "|+>" && randomBobBase === 0) {
    let tmp = Math.round(Math.random())
    return tmp === 0 ? "|0>" : "|1>"
  }
  if (receivedQubit === "|+>" && randomBobBase === 1) {
    return "|+>"
  }
  if (receivedQubit === "|->" && randomBobBase === 0) {
    let tmp = Math.round(Math.random())
    return tmp === 0 ? "|0>" : "|1>"
  }
  if (receivedQubit === "|->" && randomBobBase === 1) {
    return "|->"
  }
}

const generateTable = () => {
  table = document.createElement("table")
  tableBody = document.createElement("tbody")
  let tableHead = document.createElement("thead")
  let tableHeadRow = document.createElement("tr")

  isEva = document.querySelector('#checkbox-eva').checked

  //Table Headers
  let th1 = document.createElement("th")
  let th1Text = document.createTextNode("Bit Alice")
  th1.appendChild(th1Text)
  tableHeadRow.appendChild(th1)
  th1.style.background = '#d3290f'

  let th2 = document.createElement("th")
  let th2Text = document.createTextNode("Base Alice")
  th2.appendChild(th2Text)
  tableHeadRow.appendChild(th2)
  th2.style.background = '#d3290f'

  let th3 = document.createElement("th")
  let th3Text = document.createTextNode("Qubit Alice")
  th3.appendChild(th3Text)
  tableHeadRow.appendChild(th3)
  th3.style.background = '#d3290f'

  if (isEva) {
    let thAlt1 = document.createElement("th")
    let thAlt1Text = document.createTextNode("Base Eva")
    thAlt1.appendChild(thAlt1Text)
    tableHeadRow.appendChild(thAlt1)
    thAlt1.style.background = '#765898'

    let thAlt2 = document.createElement("th")
    let thAlt2Text = document.createTextNode("Qubit Eva")
    thAlt2.appendChild(thAlt2Text)
    tableHeadRow.appendChild(thAlt2)
    thAlt2.style.background = '#765898'
  }
  
  let th4 = document.createElement("th")
  let th4Text = document.createTextNode("Base Bob")
  th4.appendChild(th4Text)
  tableHeadRow.appendChild(th4)
  th4.style.background = '#ff8c28'

  let th5 = document.createElement("th")
  let th5Text = document.createTextNode("Qubit Bob")
  th5.appendChild(th5Text)
  tableHeadRow.appendChild(th5)
  th5.style.background = '#ff8c28'

  //Pintar row de headers en thead y pintar thead en table
  tableHead.appendChild(tableHeadRow)
  table.appendChild(tableHead)

  //Table Styles
  table.style.margin = "32px auto 8px auto"

  let inputValue = parseInt(document.querySelector('#input-value').value)
  if (isNaN(inputValue)) {
    alert("El valor que se ingreso no es un número.")
  } else {
    let pText
    for (let i = 0; i < inputValue; i++) {
      createTableRow()
    }
    let pResults = document.createElement("p")
    if (isEva) {
      if (arrayFinal.length === 0) {
        pText = document.createTextNode("✅ No hay alteracion en los bits. ✅")
      } else {
        pText = document.createTextNode("❌ Se ha(n) detectado " + arrayFinal.reduce((total, num) => total + num) + " alteracion(es) en los bits. ❌")
      }
    } else {
      pText = document.createTextNode("CLAVE: " + arrayFinal.join(""))
    }
    pResults.appendChild(pText)

    let mainContainer = document.querySelector('.main-container')
    mainContainer.appendChild(pResults)
    arrayFinal = []
  }
}


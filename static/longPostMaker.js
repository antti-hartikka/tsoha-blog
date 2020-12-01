let count = 0

        function newParagraph() {
            let idNum = count // keep track of input fields

            let newField = document.createElement("textarea") // create new text area element
            newField.setAttribute("name", idNum.toString())
            newField.setAttribute("class", "form-control")
            newField.setAttribute("rows", "3")

            let hiddenField = document.createElement("input")
            hiddenField.setAttribute("type", "hidden")
            hiddenField.setAttribute("value", "paragraph")
            hiddenField.setAttribute("name", idNum.toString() + "action")

            let br = document.createElement("br")

            // append new text field to html form
            let element = document.getElementById("fields")
            element.appendChild(br)
            element.appendChild(newField)
            element.appendChild(hiddenField)
            element.appendChild(br)

            addCount()
        }

        function newPicture() {
            addImage(count)
            addAlternative(count)
            addCount()
        }

        function addImage(idNum) {
            let newElement = document.createElement("div") // create new div element
            newElement.setAttribute("class", "form-group")

            // create label element and append div
            let label = document.createElement("label")
            label.setAttribute("for", "file")

            let text = document.createTextNode("Valitse kuva (max 500kb):")
            label.appendChild(text)

            newElement.appendChild(label)


            // create input element and append div
            let input = document.createElement("input")
            input.setAttribute("type", "file")
            input.setAttribute("class", "form-control-file")
            input.setAttribute("id", "file")
            input.setAttribute("name", idNum.toString())

            let hiddenField = document.createElement("input")
            hiddenField.setAttribute("type", "hidden")
            hiddenField.setAttribute("value", "image")
            hiddenField.setAttribute("name", idNum.toString() + "action")

            newElement.appendChild(input)
            newElement.appendChild(hiddenField)

            //let br = document.createElement("br")

            // append new fields to html form
            let element = document.getElementById("fields")
            //element.appendChild(br)
            element.appendChild(newElement)
        }

        function addAlternative(idNum) {
            let newElement = document.createElement("div") // create new div element
            newElement.setAttribute("class", "form-group")

            // create label element and append div
            let label = document.createElement("label")
            label.setAttribute("for", "text")

            let text = document.createTextNode("Vaihtoehtoinen teksti jos kuvaa ei voida näyttää:")
            label.appendChild(text)

            newElement.appendChild(label)


            // create input element and append div
            let input = document.createElement("input")
            input.setAttribute("type", "text")
            input.setAttribute("name", idNum.toString() + "a")
            input.setAttribute("class", "form-control-file")
            input.setAttribute("id", "text")

            newElement.appendChild(input)

            let br = document.createElement("br")

            // append new fields to html form
            let element = document.getElementById("fields")
            element.appendChild(br)
            element.appendChild(newElement)
        }

        function addCount() {
            count++
            let element = document.getElementById("count")
            element.setAttribute("value", count.toString())
        }

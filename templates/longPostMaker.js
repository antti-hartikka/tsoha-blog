let count = 0

        function newParagraph() {
            let idNum = count + 1 // keep track of input fields
            let newField = document.createElement("textarea") // create new text area element

            let idAttribute = document.createAttribute("id") // create new id attribute to keep count on the form elements
            idAttribute.value = idNum.toString() // set value
            newField.setAttributeNode(idAttribute) // add attribute to text field element

            // create class attribute, set value and add to text field element
            let classAttribute = document.createAttribute("class")
            classAttribute.value = "form-control"
            newField.setAttributeNode(classAttribute)

            // create attribute to rows
            let rowAttribute = document.createAttribute("rows")
            rowAttribute.value = "3"
            newField.setAttributeNode(rowAttribute)

            let br = document.createElement("br")

            // append new text field to html form
            let element = document.getElementById("fields")
            element.appendChild(br)
            element.appendChild(newField)
            element.appendChild(br)

            addCount()
        }

        function newPicture() {
            addCount()
            addImage(count)
            addAlternative(count)
        }

        function addImage(idNum) {
            let newElement = document.createElement("div") // create new div element

            let idAttribute = document.createAttribute("id") // create new id attribute to keep count on the form elements
            idAttribute.value = idNum.toString() // set value
            newElement.setAttributeNode(idAttribute) // add attribute to text field element

            // create class attribute, set value and add to text field element
            let classAttribute = document.createAttribute("class")
            classAttribute.value = "form-group"
            newElement.setAttributeNode(classAttribute)


            // create label element and append div
            let label = document.createElement("label")

            let forAtt = document.createAttribute("for")
            forAtt.value = "file"
            label.setAttributeNode(forAtt)

            let text = document.createTextNode("Valitse kuva tai video:")
            label.appendChild(text)

            newElement.appendChild(label)


            // create input element and append div
            let input = document.createElement("input")

            let typeAtt = document.createAttribute("type")
            typeAtt.value = "file"
            input.setAttributeNode(typeAtt)

            let fileClass = document.createAttribute("class")
            fileClass.value = "form-control-file"
            input.setAttributeNode(fileClass)

            let fileId = document.createAttribute("id")
            fileId.value = "file"
            input.setAttributeNode(fileId)

            newElement.appendChild(input)


            //let br = document.createElement("br")

            // append new fields to html form
            let element = document.getElementById("fields")
            //element.appendChild(br)
            element.appendChild(newElement)
        }

        function addAlternative(idNum) {
            let newElement = document.createElement("div") // create new div element

            let idAttribute = document.createAttribute("id") // create new id attribute to keep count on the form elements
            idAttribute.value = idNum.toString() + "a" // set value
            newElement.setAttributeNode(idAttribute) // add attribute to text field element

            // create class attribute, set value and add to text field element
            let classAttribute = document.createAttribute("class")
            classAttribute.value = "form-group"
            newElement.setAttributeNode(classAttribute)


            // create label element and append div
            let label = document.createElement("label")

            let forAtt = document.createAttribute("for")
            forAtt.value = "text"
            label.setAttributeNode(forAtt)

            let text = document.createTextNode("Anna kuvalle vaihtoehtoinen teksti:")
            label.appendChild(text)

            newElement.appendChild(label)


            // create input element and append div
            let input = document.createElement("input")

            let typeAtt = document.createAttribute("type")
            typeAtt.value = "text"
            input.setAttributeNode(typeAtt)

            let fileClass = document.createAttribute("class")
            fileClass.value = "form-control-file"
            input.setAttributeNode(fileClass)

            let fileId = document.createAttribute("id")
            fileId.value = "text"
            input.setAttributeNode(fileId)

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
            element.setAttribute("name", count.toString())
        }

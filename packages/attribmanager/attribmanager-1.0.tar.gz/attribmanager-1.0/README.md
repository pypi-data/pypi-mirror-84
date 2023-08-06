# attribmanager

##### A simple pythonic module to lock (make read-only) and hide class attributes


## Installation

`pip install attribmanager`

## Usage

```
import attribmanger

class example(attribmanger.manage):

	def __init__(self):

		self.mylist = ["item 1", "item2"]
		self.lock("mylist")
		# mylist is read only and cannot be edited now, changing it
		# will raise an error, 
		
		self.myvar = "foo"
		self.hide("myvar")
		# myvar will not show up anywhere, and cannot be edited
		
		self.unhide("myvar")
		# Hiding an object without being able to unhide it would be
		# the same as deleting it, that's why you can unhide it
```
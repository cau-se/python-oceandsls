model eval

types
	enum Color { red, green, blue }
	range Temperature float [ 0 : 373 ]
	
feature general : "feature general description" {
	group settings : "group settings" {
		def color Color : "color"
	}
	sub multiple
		feature pump : "pumping station" {
			group settings2 : "second settings" {
				def temperature Temperature : kelvin
			}
		}
		feature pipe : "pipes"
}
feature offline : "the disabled one" {
}



group common : "Common Description" {
	def ground_temp Temperature : kelvin
	def ground_color Color : ""
}

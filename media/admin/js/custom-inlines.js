/**
 * Django admin inlines
 *
 * Based on jQuery Formset 1.1
 * @author Stanislaus Madueke (stan DOT madueke AT gmail DOT com)
 * @requires jQuery 1.2.6 or later
 *
 * Copyright (c) 2009, Stanislaus Madueke
 * All rights reserved.
 *
 * Spiced up with Code from Zain Memon's GSoC project 2009
 * and modified for Django by Jannis Leidel
 *
 * Licensed under the New BSD License
 * See: http://www.opensource.org/licenses/bsd-license.php
 */
(function($) {
	//This function use jQuery and django.jQuery because of bootstrap template and django.
	$.fn.formset = function(opts) {
		var options = $.extend({}, $.fn.formset.defaults, opts);
		var updateElementIndex = function(el, prefix, ndx) {
			var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
			var replacement = prefix + "-" + ndx;
			if ($(el).attr("for")) {
				$(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
			}
			if (el.id) {
				el.id = el.id.replace(id_regex, replacement);
			}
			if (el.name) {
				el.name = el.name.replace(id_regex, replacement);
			}
		};
		var totalForms = $("#id_" + options.prefix + "-TOTAL_FORMS").attr("autocomplete", "off");
		var nextIndex = parseInt(totalForms.val());
		var maxForms = $("#id_" + options.prefix + "-MAX_NUM_FORMS").attr("autocomplete", "off");
		// only show the add button if we are allowed to add more items,
        // note that max_num = None translates to a blank string.
		var showAddButton = maxForms.val() == '' || (maxForms.val()-totalForms.val()) > 0;
		$(this).each(function(i) {
			$(this).not("." + options.emptyCssClass).addClass(options.formCssClass);
		});
		if ($(this).length && showAddButton) {
			var addButton;
			//REAL_ESTATE_APP: Custom addButtonCreate
			if (options.addButtonCreate) {
				if ($(this).attr("tagName") == "TR") {
					// If forms are laid out as table rows, insert the
					// "add" button in a new table row:
					var numCols = this.eq(0).children().length;
					$(this).parent().append('<tr class="' + options.addCssClass + '"><td colspan="' + numCols + '"><a href="javascript:void(0)">' + options.addText + "</a></tr>");
					addButton = $(this).parent().find("tr:last a");
				} else {
					// Otherwise, insert it immediately after the last form:
					$(this).filter(":first").before('<div class="' + options.addCssClass + '"><a class="btn btn-primary" href="javascript:void(0)"><i class="icon-plus icon-white"></i>' + options.addText + "</a></div>");
					addButton = $(this).filter(":first").parent().find("a");
				}
			} else {
				//REAL_ESTATE_APP: custom addButton get on group.
				addButton = $('#'+options.prefix+'-group').find('.'+options.addCssClass);
			}
			addButton.click(function() {
				// REAL_ESTATE_APP: custom bootstrap collapse hide a photo edited
				var editInline = $('#'+options.prefix+'-group').find('.in').collapse('hide');
				
				var totalForms = $("#id_" + options.prefix + "-TOTAL_FORMS");
				var template = $("#" + options.prefix + "-empty");
				//This active bootstrap-datetimepicker when a template is cloned.
				template.find('div#time-widget').datetimepicker('destroy');
				template.find('div#date-widget').datetimepicker('destroy');

				var row = template.clone(true);

				//This active bootstrap-datetimepicker when a template is cloned.
				row.find('div#time-widget').datetimepicker({
		      			pickDate: false,
		    	});
		    	row.find('div#date-widget').datetimepicker({
		      			pickTime: false,
		      	});

				row.removeClass(options.emptyCssClass)
				    .addClass(options.formCssClass)
				    .attr("id", options.prefix + "-" + nextIndex);
				if (row.is("tr")) {
					// If the forms are laid out in table rows, insert
					// the remove button into the last table cell:
					row.children(":last").append('<div><a class="' + options.deleteCssClass +'" href="javascript:void(0)">' + options.deleteText + "</a></div>");
				} else if (row.is("ul") || row.is("ol")) {
					// If they're laid out as an ordered/unordered list,
					// insert an <li> after the last list item:
					row.append('<li><a class="' + options.deleteCssClass +'" href="javascript:void(0)">' + options.deleteText + "</a></li>");
				} else {
					// Otherwise, just insert the remove button as the
					// last child element of the form's container:
					row.children(":first").append('<a class="btn btn-danger pull-right ' + options.deleteCssClass + '" href="javascript:void(0)"><i class="icon-remove icon-white"></i> ' + options.deleteText + "</a>");
				}
				row.find("*").each(function() {
					updateElementIndex(this, options.prefix, totalForms.val());
				});
				// Insert the new form when it has been fully edited
				row.insertBefore($(template));
				// Update number of total forms
				$(totalForms).val(parseInt(totalForms.val()) + 1);

				nextIndex += 1;
				// Hide add button in case we've hit the max, except we want to add infinitely
				if ((maxForms.val() != '') && (maxForms.val()-totalForms.val()) <= 0) {
					addButton.hide();
				}

				// The delete button of each row triggers a bunch of other things
				row.find("a." + options.deleteCssClass).click(function() {
					// Remove the parent form containing this button:
					var row = $(this).parents("." + options.formCssClass);
					row.remove();
					nextIndex -= 1;

					// If a post-delete callback was provided, call it with the deleted form:
					if (options.removed) {
						options.removed(row);
					}
					// Update the TOTAL_FORMS form count.
					var forms = $("." + options.formCssClass);
					$("#id_" + options.prefix + "-TOTAL_FORMS").val(forms.length);
					// Show add button again once we drop below max
					if ((maxForms.val() == '') || (maxForms.val()-forms.length) > 0) {
						addButton.show();
					}
					// Also, update names and ids for all remaining form controls
					// so they remain in sequence:
					for (var i=0, formCount=forms.length; i<formCount; i++)
					{
						updateElementIndex($(forms).get(i), options.prefix, i);
						$(forms.get(i)).find("*").each(function() {
							updateElementIndex(this, options.prefix, i);
						});
					}
					return false;
				});
				// If a post-add callback was supplied, call it with the added form:
				if (options.added) {
					options.added(row);
				}

				return false;
			});
		}
		if (options.inited) {
			options.inited(this);
		}
		return this;
	}
	/* Setup plugin defaults */
	$.fn.formset.defaults = {
		prefix: "form",					// The form prefix for your django formset
		addText: "add another",			// Text for the add link
		deleteText: "remove",			// Text for the delete link
		addCssClass: "add-row",			// CSS class applied to the add link
		deleteCssClass: "delete-row",	// CSS class applied to the delete link
		emptyCssClass: "empty-row",		// CSS class applied to the empty row
		formCssClass: "dynamic-form",	// CSS class applied to each form in a formset
		added: null,					// Function called each time a new form is added
		removed: null,					// Function called each time a form is deleted
		addButtonCreate: true,			// CUSTOM REAL_ESTATE_APP: Create automatic add button
		inited: null,					// CUSTOM REAL_ESTATE_APP: Init functions
	}
})(jQuery);

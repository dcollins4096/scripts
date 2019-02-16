
import jinja2
loader=jinja2.FileSystemLoader('.')
env = jinja2.Environment(loader=loader)
template = env.get_template('budget_template_1.html')
foutptr = open(fname,'w')
foutptr.write( template.render(fixies=fixies,amounts=amounts,
                               floaters=floaters))
foutptr.close()
"""
HTML Template Blank:
mostly 
{% for d in list_of_days%}
      <tr><td> {{d.date.month}} / {{d.date.day}}</td>
          <td> {{d.pending_items}}</td>
          <td> {{d.expected_item}}</td>
          <td>{{d.remaining_items}}</td>
          <td style = {{d.css_remaining}}>{{d.remaining_balance}}</td>
          <td style = {{d.css_remaining_perdiem}}>{{d.remaining_balance_with_perdiem}}</td>
          <!-- <td style =
              {{d.css_budget_health}}>{{d.budget_health}} </td>  -->
      </tr>
      {% endfor %}
""""
         


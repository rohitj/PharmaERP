﻿
<form id="frmDistt">
    {{ formset.management_form }}

<table id="Distt">

    {% for form in formset %}
       {% if forloop.counter == 1  %}
       <tr>
            {% for field in form %}
           <td> {{ field.label_tag }}  </td>
            {% endfor %}

       </tr>
       {% endif %}
      <tr>

      {% for field in form %}
          <td> {{ field }}  > </td>
      {% endfor %}

          <td> <input type="text" name="status{{ forloop.counter }}" readonly > </td>
          <td> <button id="Dist" >Change </button>  </td>


     </tr>

    {% endfor %}

    <tr>
        <td> <p> <span id="total" style="color:blue" >Total quantity </span>  </p></td>
        <td><input type="text" id="totalqty" readonly ></td>
        <td> </td>
        <td></td>
    </tr>

</table>


</body>
</form>


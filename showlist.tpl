% include("header.tpl")

<p>All notes:</p>
<table border="1">
<tr>
    <th>id</th>
    <th>заметка</th>
    <th>private</th>
    <th>key</th>
    <th>edit</th>
</tr>
%for row in rows:
  <tr>
  %(id, note, priv, key) = row
    <td>{{id}}</td>
    <td>
        <p>
            {{note}}
        </p>
    </td>
    <td>
        {{priv}}
    </td>
    <td>
        {{key}}
    </td>
    <td>
        <a href="/edit/{{id}}">Edit</a>
    </td>
  </tr>
%end
</table>

<p>Редактирование по ключу:</p>
<form action="/key/" method="GET">
    <div>
        <input size="20" maxlength="20" name="key" value=""/>
        <input type="submit" name="edit" value="Редактировать"/>
    </div>
</form>

% include("footer.tpl")
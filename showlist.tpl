<form action="/edit" method="GET">
    <input type="submit" name="add" value="add">
</form>
<p>All notes:</p>
<table border="1">
<tr>
    <th>id</th>
    <th>заметка</th>
    <th>private</th>
    <th>edit</th>
</tr>
%for row in rows:
  <tr>
  %(id, note, priv) = row
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
        <a href="/edit/{{id}}">Edit</a>
    </td>
  </tr>
%end
</table>

<p>Редактирование по ключу:</p>
<form action="/bykey/" method="GET">
    <div>
        <input size="20" maxlength="20" name="key" value=""/>
        <input type="submit" name="edit" value="Редактировать"/>
    </div>
</form>
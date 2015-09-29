<p>Список заметок</p>

%for row in rows:
  <div class="notecontent">
  %(id, note, priv, key) = row
    <div>
      <span>
	  <a href="/edit/{{id}}">Редактировать</a>
      </span>
      <span>
	  {{priv}}
      </span>
      <span>
	  {{key}}
      </span>
    </div>
    <div>
        <p><pre>
            {{note}}
        </pre></p>
    </div>
  </div>
%end

<p>Редактирование по ключу:</p>
<form action="/key/" method="GET">
    <div>
        <input size="32" maxlength="32" name="key" value=""/>
        <input type="submit" name="edit" value="Редактировать"/>
    </div>
</form>
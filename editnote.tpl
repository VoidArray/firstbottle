%if (id == 0):
    <p>Добавление новой заметки</p>
%else:
    <p>Редактирование</p>
%end
<form action="/save" method="GET">
    <div>
        <p>Приватная?</b>
        %if private:
            <input type="checkbox" checked="checked" name="private"/>
        %else:
            <input type="checkbox" name="private"/>
        %end
    </div>
    <div>
        <textarea rows="10" cols="30" name="note">{{note}}</textarea>
    </div>
    <div>
        <input type="submit" name="save" value="save"/>
    </div>
    <div>
        <input type="hidden" name="key" value="{{id}}"/>
    </div>
</form>
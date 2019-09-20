# -*- coding: utf-8 -*-

import sys
import dbf
import warnings
import traceback
import struct
from dbf import Table

from dbf import DbfError, input_decoding, READ_WRITE, FieldType, \
    FieldSpecError, FieldNameWarning, NULLABLE, scatter


def add_fields(self, field_specs):
    """
    adds field(s) to the table layout; format is Name Type(Length,Decimals)[; Name Type(Length,Decimals)[...]]
    backup table is created with _backup appended to name
    then zaps table, recreates current structure, and copies records back from the backup
    """
    # for python 2, convert field_specs from bytes to unicode if necessary
    if isinstance(field_specs, bytes):
        if input_decoding is None:
            raise DbfError(
                'field specifications must be in unicode (or set input_decoding)')
        field_specs = field_specs.decode(input_decoding)
    if isinstance(field_specs, list) and any(
            isinstance(t, bytes) for t in field_specs):
        if input_decoding is None:
            raise DbfError(
                'field specifications must be in unicode (or set input_decoding)')
        fs = []
        for text in field_specs:
            if isinstance(text, bytes):
                text = text.decode(input_decoding)
            fs.append(text)
        field_specs = fs
    meta = self._meta
    if meta.status != READ_WRITE:
        raise DbfError(
            '%s not in read/write mode, unable to add fields (%s)' % (
            meta.filename, meta.status))
    fields = self.structure()
    original_fields = len(fields)
    fields += self._list_fields(field_specs, sep=u';')
    null_fields = any(['null' in f.lower() for f in fields])
    if (len(fields) + null_fields) > meta.max_fields:
        raise DbfError(
            "Adding %d more field%s would exceed the limit of %d"
            % (len(fields), ('', 's')[len(fields) == 1], meta.max_fields)
        )
    old_table = None
    if self:
        old_table = self.create_backup()
        self.zap()
    if meta.mfd is not None and not meta.ignorememos:
        meta.mfd.close()
        meta.mfd = None
        meta.memo = None
    if not meta.ignorememos:
        meta.newmemofile = True
    offset = 1
    for name in meta.fields:
        del meta[name]
    meta.fields[:] = []

    meta.blankrecord = None
    null_index = -1
    for field_seq, field in enumerate(fields):
        if not field:
            continue
        field = field.lower()
        pieces = field.split()
        name = pieces.pop(0)
        try:
            if '(' in pieces[0]:
                loc = pieces[0].index('(')
                pieces.insert(0, pieces[0][:loc])
                pieces[1] = pieces[1][loc:]
            format = FieldType(pieces.pop(0))
            if pieces and '(' in pieces[0]:
                for i, p in enumerate(pieces):
                    if ')' in p:
                        pieces[0:i + 1] = [''.join(pieces[0:i + 1])]
                        break
        except IndexError:
            raise FieldSpecError('bad field spec: %r' % field)
        if field_seq >= original_fields and (
                name[0] == '_' or name[0].isdigit() or not name.replace('_',
                                                                        '').isalnum()):
            # find appropriate line to point warning to
            for i, frame in enumerate(reversed(traceback.extract_stack()),
                                      start=1):
                if frame[0] == __file__ and frame[2] == 'resize_field':
                    # ignore
                    break
                elif frame[0] != __file__ or frame[2] not in (
                '__init__', 'add_fields'):
                    warnings.warn(
                        '"%s invalid:  field names should start with a letter, and only contain letters, digits, and _' % name,
                        FieldNameWarning, stacklevel=i)
                    break
        if name in meta.fields:
            raise DbfError("Field '%s' already exists" % name)
        field_type = format
        if len(name) > 20:
            raise FieldSpecError(
                "Maximum field name length is 20.  '%s' is %d characters "
                "long." % (
                name, len(name)))
        if not field_type in meta.fieldtypes.keys():
            raise FieldSpecError("Unknown field type:  %s" % field_type)
        init = self._meta.fieldtypes[field_type]['Init']
        flags = self._meta.fieldtypes[field_type]['flags']
        try:
            length, decimals, flags = init(pieces, flags)
        except FieldSpecError:
            exc = sys.exc_info()[1]
            raise FieldSpecError(
                exc.message + ' (%s:%s)' % (meta.filename, name)).from_None()
        nullable = flags & NULLABLE
        if nullable:
            null_index += 1
        start = offset
        end = offset + length
        offset = end
        meta.fields.append(name)
        cls = meta.fieldtypes[field_type]['Class']
        empty = meta.fieldtypes[field_type]['Empty']
        meta[name] = (
            field_type,
            start,
            length,
            end,
            decimals,
            flags,
            cls,
            empty,
            nullable and null_index,
        )
    self._build_header_fields()
    self._update_disk()
    if old_table is not None:
        old_table.open()
        for record in old_table:
            self.append(scatter(record))
        old_table.close()


Table.add_fields = add_fields


def pack_str(string):
    """
    Returns an 11 byte, upper-cased, null padded string suitable for field names;
    raises DbfError if the string is bigger than 10 bytes
    """
    if len(string) > 20:
        raise DbfError("Maximum string size is 20 characters -- %s has %d "
                       "characters" % (string, len(string)))
    return struct.pack('11s', string.upper())

dbf.pack_str = pack_str